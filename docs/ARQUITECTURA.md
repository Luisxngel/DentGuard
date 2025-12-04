# Arquitectura de DentalGuard ERP

## Visión General
DentalGuard ERP es un sistema de gestión para clínicas dentales diseñado para ser modular, escalable y fácil de mantener. La aplicación utiliza **Streamlit** para la interfaz de usuario, lo que permite un desarrollo rápido y una experiencia de usuario fluida.

## Flujo de Datos
1.  **Usuario**: Interactúa con la interfaz web (Streamlit).
2.  **Frontend (Streamlit)**:
    *   Maneja la entrada del usuario.
    *   Gestiona el estado de la sesión (`st.session_state`).
    *   Renderiza componentes UI desde `src/components`.
3.  **Capa de Lógica (Python)**:
    *   `src/auth`: Valida credenciales y permisos.
    *   `app.py`: Orquesta la navegación y el diseño principal.
4.  **Capa de Datos**:
    *   `src/data`: Abstracción para operaciones de base de datos (actualmente SQLite).
5.  **Servicios Externos**:
    *   `src/utils/ai_core.py`: Conecta con la API de Groq para funcionalidades de IA.

## Estructura de Directorios
*   `/src`: Código fuente principal.
    *   `/auth`: Autenticación y autorización.
    *   `/components`: Componentes UI reutilizables.
    *   `/data`: Modelos y acceso a datos.
    *   `/utils`: Utilidades y clientes externos.
*   `/docs`: Documentación del proyecto.
*   `/tests`: Pruebas automatizadas.

## Tecnologías Clave
*   **Frontend/Backend**: Python + Streamlit
*   **Base de Datos**: SQLite (MVP) -> PostgreSQL (Futuro)
*   **IA**: Groq API
*   **Autenticación**: Custom (MVP) -> OAuth/JWT (Futuro)
