import json
import os

SETTINGS_FILE = "assets/settings.json"

DEFAULT_SETTINGS = {
    "nombre_clinica": "DentalGuard Clinic",
    "slogan": "Especialistas en Sonrisas",
    "direccion": "Av. Salud 123, Ciudad Médica",
    "telefono": "555-0199",
    "mensaje_pie": "Gracias por su visita"
}

def load_settings():
    if not os.path.exists(SETTINGS_FILE):
        return DEFAULT_SETTINGS
    
    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return DEFAULT_SETTINGS

def save_settings(data):
    # Ensure assets directory exists
    os.makedirs(os.path.dirname(SETTINGS_FILE), exist_ok=True)
    
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
