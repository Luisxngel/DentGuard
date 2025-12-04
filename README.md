# DentalGuard ERP

Sistema de gestión integral para clínicas dentales, potenciado con IA.

## Características
- **Gestión de Pacientes:** Base de datos persistente (SQLite).
- **IA Consultor:** Chatbot médico integrado (Groq API) con contexto clínico.
- **Roles y Seguridad:** Panel de Admin vs. Panel de Doctor (RBAC).
- **Interfaz Moderna:** UI limpia diseñada para entornos médicos.
## Instalación

1.  **Clonar el repositorio** (o descargar los archivos):
    ```bash
    # (Si usas git)
    git clone https://github.com/Luisxngel/DentGuard.git
    cd DentGuard
    ```

2.  **Crear un entorno virtual (recomendado)**:
    ```bash
    python -m venv venv
    # Windows
    .\venv\Scripts\activate
    # Linux/Mac
    source venv/bin/activate
    ```

3.  **Instalar dependencias**:
    ```bash
    pip install -r requirements.txt
    ```

## Uso

1.  **Ejecutar la aplicación**:
    ```bash
    streamlit run app.py
    ```

2.  **Credenciales por defecto (MVP)**:
    *   **Admin**: `admin` / `admin123`
    *   **Doctor**: `doctor` / `doc123`

## Estructura del Proyecto
Ver `/docs/ARQUITECTURA.md` para más detalles.
