import streamlit as st
import os
from src.auth.login import login_user
from src.utils.ai_core import test_connection, consultar_ia
from src.data.database import init_db, add_paciente, get_pacientes

# Configuración de la página
st.set_page_config(
    page_title="DentalGuard ERP",
    page_icon="🦷",
    layout="wide"
)

# Inicializar Base de Datos
init_db()

# Inicializar estado de sesión
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user = None
    st.session_state.role = None

def main():
    if not st.session_state.logged_in:
        show_login_screen()
    else:
        show_dashboard()

def show_login_screen():
    st.title("🦷 DentalGuard ERP")
    st.subheader("Iniciar Sesión")
    
    col1, col2 = st.columns([1, 2])
    with col1:
        username = st.text_input("Usuario")
        password = st.text_input("Contraseña", type="password")
        
        if st.button("Entrar", type="primary"):
            user = login_user(username, password)
            if user:
                st.session_state.logged_in = True
                st.session_state.user = user
                st.session_state.role = user["role"]
                st.success(f"Bienvenido, {user['name']}")
                st.rerun()
            else:
                st.error("Usuario o contraseña incorrectos")

    with col2:
        st.info("Credenciales Demo:\n- Admin: admin / admin123\n- Doctor: doctor / doc123")

def render_patient_management():
    st.subheader("Gestión Clínica")
    tab1, tab2 = st.tabs(["Registrar Paciente", "Ver Pacientes"])
    
    with tab1:
        with st.form("new_patient"):
            nombre = st.text_input("Nombre Completo")
            edad = st.number_input("Edad", min_value=0, max_value=120)
            historial = st.text_area("Historial Médico")
            submitted = st.form_submit_button("Guardar Paciente")
            
            if submitted:
                add_paciente(nombre, edad, historial)
                st.success("Paciente registrado correctamente.")
    
    with tab2:
        st.subheader("Listado de Pacientes")
        df_pacientes = get_pacientes()
        # Fix deprecation warning
        st.dataframe(df_pacientes, width='stretch') 
        
        if not df_pacientes.empty:
            st.markdown("### Consultar IA sobre Pacientes")
            pregunta = st.text_input("Pregunta a la IA:")
            if st.button("Consultar"):
                respuesta = consultar_ia(pregunta)
                st.info(respuesta)

def show_dashboard():
    # Sidebar dinámico según rol
    with st.sidebar:
        logo_path = "assets/logo.png"
        if os.path.exists(logo_path):
            st.image(logo_path, width=200)
        else:
            st.header("🦷 DentalGuard")

        st.title(f"Panel {st.session_state.role.capitalize()}")
        st.write(f"👤 {st.session_state.user['name']}")
        
        if st.button("Cerrar Sesión"):
            st.session_state.logged_in = False
            st.session_state.user = None
            st.session_state.role = None
            st.rerun()
        
        st.markdown("---")
        st.subheader("Navegación")
        
        view_mode = "Inicio"
        
        if st.session_state.role == "admin":
            # God Mode: Admin sees everything
            view_mode = st.radio("Ir a:", ["Admin Panel", "Clínica", "Configuración"])
        elif st.session_state.role == "doctor":
            view_mode = st.radio("Ir a:", ["Clínica", "Perfil"])
        else:
            view_mode = st.radio("Ir a:", ["Inicio"])

    # Contenido principal
    st.title("DentalGuard ERP - Dashboard")
    st.caption(f"Estado IA: {test_connection()}")
    
    if view_mode == "Admin Panel":
        st.info("Vista de Administrador - Control Total")
        st.metric("Total Pacientes", len(get_pacientes()))
        # More admin widgets here...
        
    elif view_mode == "Clínica":
        render_patient_management()
        
    elif view_mode == "Configuración":
        st.warning("Configuración del Sistema (Solo Admin)")
        
    elif view_mode == "Perfil":
        st.info(f"Perfil de {st.session_state.user['name']}")

if __name__ == "__main__":
    main()
