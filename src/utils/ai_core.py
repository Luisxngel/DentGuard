import streamlit as st
from groq import Groq
from src.data.database import get_pacientes

def get_groq_client():
    """
    Inicializa el cliente de Groq de forma segura usando st.secrets.
    Retorna None si no hay configuración.
    """
    try:
        # Intenta obtener la key de secrets.toml
        api_key = st.secrets["GROQ_API_KEY"]
        return Groq(api_key=api_key)
    except Exception as e:
        # Fallback silencioso o log de error
        print(f"Error configurando Groq: {e}")
        return None

def test_connection():
    client = get_groq_client()
    if client:
        return "Conexión a Groq lista."
    return "Groq no configurado (Revisar .streamlit/secrets.toml)."

def obtener_contexto_db():
    """Recupera datos relevantes de la BD para dar contexto a la IA."""
    try:
        df = get_pacientes()
        if df.empty:
            return "No hay pacientes registrados aún."
        
        # Convertir a string simple
        contexto = "Lista de Pacientes:\n"
        for _, row in df.iterrows():
            contexto += f"- ID {row['id']}: {row['nombre']} ({row['edad']} años). Historial: {row['historial']}\n"
        return contexto
    except Exception as e:
        return f"Error al recuperar contexto: {str(e)}"

def consultar_ia(prompt, contexto_adicional=""):
    client = get_groq_client()
    if not client:
        return "Error: Sistema de IA no configurado. Verifica tu API Key."
    
    # Inyectar contexto de la base de datos
    db_context = obtener_contexto_db()
    full_context = f"{contexto_adicional}\n\nDatos del Sistema:\n{db_context}"
    
    try:
        chat = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "Eres un asistente dental experto. Usa la información de los pacientes proporcionada para responder con precisión."},
                {"role": "user", "content": f"Contexto: {full_context}\n\nPregunta: {prompt}"}
            ],
            model="llama-3.3-70b-versatile",
        )
        return chat.choices[0].message.content
    except Exception as e:
        return f"Error de conexión neuronal: {str(e)}"
