import streamlit as st
import os
import time
from datetime import datetime
from src.auth.login import login_user
from src.utils.ai_core import test_connection, consultar_ia
from src.utils.pdf_gen import generar_receta_pdf
from src.data.database import init_db, add_paciente, get_pacientes, add_imagen, get_imagenes, add_transaccion, get_finanzas, get_deudas_pendientes, saldar_deuda

# Configuración de la página
st.set_page_config(
    page_title="DentalGuard ERP",
    page_icon="🦷",
    layout="wide"
)

# Inicializar Base de Datos
init_db()

# Asegurar directorios de assets
if not os.path.exists("assets/uploads"):
    os.makedirs("assets/uploads")

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
    tab1, tab2, tab3, tab4 = st.tabs(["Registrar Paciente", "Ver Pacientes", "Imágenes / Rayos X", "Generar Receta"])
    
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

    with tab3:
        st.subheader("Galería de Imágenes")
        df_pacientes = get_pacientes()
        
        if df_pacientes.empty:
            st.warning("No hay pacientes registrados.")
        else:
            # Selector de paciente
            paciente_opciones = df_pacientes.set_index('id')['nombre'].to_dict()
            selected_id = st.selectbox("Seleccionar Paciente", options=paciente_opciones.keys(), format_func=lambda x: paciente_opciones[x])
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### Subir Nueva Imagen")
                uploaded_file = st.file_uploader("Cargar Rayos X / Foto", type=['png', 'jpg', 'jpeg'])
                tipo_imagen = st.selectbox("Tipo de Imagen", ["Rayos X", "Foto Intraoral", "Documento", "Otro"])
                
                if uploaded_file is not None:
                    if st.button("Guardar Imagen"):
                        # Crear directorio si no existe (redundancia segura)
                        save_dir = "assets/uploads"
                        if not os.path.exists(save_dir):
                            os.makedirs(save_dir)
                        
                        # Generar nombre único
                        file_ext = uploaded_file.name.split('.')[-1]
                        filename = f"{selected_id}_{int(time.time())}.{file_ext}"
                        file_path = os.path.join(save_dir, filename)
                        
                        # Guardar archivo
                        with open(file_path, "wb") as f:
                            f.write(uploaded_file.getbuffer())
                        
                        # Registrar en DB
                        # FIX: Normalizar ruta para evitar errores en Windows (Backslashes)
                        ruta_normalizada = file_path.replace("\\", "/")
                        add_imagen(selected_id, ruta_normalizada, tipo_imagen)
                        st.success("Imagen guardada correctamente.")
                        st.rerun()

            with col2:
                st.markdown("#### Galería del Paciente")
                df_imgs = get_imagenes(selected_id)
                
                if df_imgs.empty:
                    st.info("No hay imágenes registradas para este paciente.")
                else:
                    # Mostrar grid de imágenes
                    for _, img in df_imgs.iterrows():
                        ruta = img['ruta_archivo']
                        if os.path.exists(ruta):
                            st.image(ruta, caption=f"{img['tipo']} - {img['fecha']}", width=300)
                        else:
                            st.warning(f"Imagen no encontrada: {ruta}")

    with tab4:
        st.subheader("Generar Receta Médica")
        df_pacientes = get_pacientes()
        
        if df_pacientes.empty:
            st.warning("No hay pacientes registrados.")
        else:
            # Selector de paciente (Reutilizado)
            paciente_opciones = df_pacientes.set_index('id')['nombre'].to_dict()
            selected_id_rx = st.selectbox("Paciente", options=paciente_opciones.keys(), format_func=lambda x: paciente_opciones[x], key="rx_patient")
            paciente_nombre = paciente_opciones[selected_id_rx]
            
            with st.form("receta_form"):
                diagnostico = st.text_input("Diagnóstico")
                medicamentos = st.text_area("Medicamentos e Indicaciones", height=150)
                submitted_rx = st.form_submit_button("Preparar Receta")
                
            if submitted_rx:
                if not diagnostico or not medicamentos:
                    st.error("Por favor complete todos los campos.")
                else:
                    # Generar PDF
                    pdf_buffer = generar_receta_pdf(
                        doctor_nombre=st.session_state.user['name'],
                        paciente_nombre=paciente_nombre,
                        fecha=time.strftime("%d/%m/%Y"),
                        diagnostico=diagnostico,
                        medicamentos=medicamentos
                    )
                    
                    st.success("Receta generada exitosamente.")
                    st.download_button(
                        label="📥 Descargar Receta PDF",
                        data=pdf_buffer,
                        file_name=f"Receta_{paciente_nombre.replace(' ', '_')}.pdf",
                        mime="application/pdf"
                    )

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
            view_mode = st.radio("Ir a:", ["Admin Panel", "Finanzas", "Clínica", "Configuración"])
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
        
    elif view_mode == "Finanzas":
        st.subheader("Módulo Financiero")
        
        # --- KPIs ---
        df_finanzas = get_finanzas()
        
        # Calcular métricas
        total_ingresos = 0
        total_gastos = 0
        total_por_cobrar = 0
        
        if not df_finanzas.empty:
            # Ingresos Pagados
            ingresos_df = df_finanzas[(df_finanzas['tipo'] == 'Ingreso') & (df_finanzas['estado'] == 'Pagado')]
            total_ingresos = ingresos_df['monto'].sum()
            
            # Gastos (siempre pagados en este modelo simple)
            gastos_df = df_finanzas[df_finanzas['tipo'] == 'Gasto']
            total_gastos = gastos_df['monto'].sum()
            
            # Por Cobrar (Ingresos Pendientes)
            pendientes_df = df_finanzas[(df_finanzas['tipo'] == 'Ingreso') & (df_finanzas['estado'] == 'Pendiente')]
            total_por_cobrar = pendientes_df['monto'].sum()
            
        caja_real = total_ingresos - total_gastos
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Caja Real", f"S/. {caja_real:,.2f}")
        col2.metric("Por Cobrar (Deuda)", f"S/. {total_por_cobrar:,.2f}", delta_color="inverse")
        col3.metric("Gastos Operativos", f"S/. {total_gastos:,.2f}", delta_color="inverse")
        
        st.markdown("---")
        
        # --- Pestañas ---
        tab_reg, tab_cob, tab_hist = st.tabs(["📝 Registrar", "🔔 Cuentas por Cobrar", "📊 Historial Completo"])
        
        # TAB 1: Registrar
        with tab_reg:
            st.markdown("#### Registrar Movimiento")
            with st.form("finance_form"):
                col_a, col_b = st.columns(2)
                with col_a:
                    tipo_mov = st.selectbox("Tipo", ["Ingreso", "Gasto"])
                    monto = st.number_input("Monto", min_value=0.0, step=10.0)
                with col_b:
                    concepto = st.text_input("Concepto")
                    fecha_mov = st.date_input("Fecha", value=datetime.now())
                
                # Lógica condicional simulada
                es_credito = st.checkbox("¿Es Crédito / Deuda?")
                
                # Selector de paciente
                df_p = get_pacientes()
                paciente_id = None
                if not df_p.empty:
                    opciones = {p['id']: p['nombre'] for _, p in df_p.iterrows()}
                    opciones[0] = "Ninguno / General" 
                    pid_sel = st.selectbox("Paciente Asociado", options=list(opciones.keys()), format_func=lambda x: opciones[x])
                    if pid_sel != 0:
                        paciente_id = pid_sel
                
                submitted_fin = st.form_submit_button("Registrar Transacción")
                
                if submitted_fin:
                    estado = "Pagado"
                    if tipo_mov == "Ingreso" and es_credito:
                        estado = "Pendiente"
                        if paciente_id is None:
                            st.error("Debe asociar un paciente para registrar una deuda.")
                            st.stop()
                    
                    add_transaccion(tipo_mov, monto, concepto, fecha_mov, paciente_id, estado)
                    st.success("Movimiento registrado.")
                    st.rerun()

        # TAB 2: Cobranza
        with tab_cob:
            st.markdown("#### Gestión de Cobranza")
            df_deudas = get_deudas_pendientes()
            
            if df_deudas.empty:
                st.balloons()
                st.success("¡Excelente! No hay deudas pendientes.")
            else:
                for index, row in df_deudas.iterrows():
                    c1, c2, c3, c4 = st.columns([2, 3, 2, 2])
                    c1.write(row['fecha'])
                    c2.write(f"{row['paciente_nombre']} - {row['concepto']}")
                    c3.write(f"**S/. {row['monto']:,.2f}**")
                    if c4.button(f"Saldar", key=f"pay_{row['id']}"):
                        saldar_deuda(row['id'])
                        st.success(f"Deuda de {row['paciente_nombre']} saldada.")
                        st.rerun()

        # TAB 3: Historial
        with tab_hist:
            st.markdown("#### Historial de Transacciones")
            if df_finanzas.empty:
                st.info("No hay transacciones registradas.")
            else:
                # Ordenar por fecha descendente
                df_display = df_finanzas.sort_values(by='fecha', ascending=False)
                
                # Formatear columnas para visualización
                st.dataframe(
                    df_display[['fecha', 'tipo', 'concepto', 'monto', 'estado']],
                    column_config={
                        "monto": st.column_config.NumberColumn(
                            "Monto",
                            format="S/. %.2f"
                        )
                    },
                    use_container_width=True,
                    hide_index=True
                )

    elif view_mode == "Clínica":
        render_patient_management()
        
    elif view_mode == "Configuración":
        st.warning("Configuración del Sistema (Solo Admin)")
        
    elif view_mode == "Perfil":
        st.info(f"Perfil de {st.session_state.user['name']}")

if __name__ == "__main__":
    main()
