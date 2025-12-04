import time

# Base de datos de usuarios simulada
USERS_DB = {
    "admin": {
        "password": "admin123", # En producción, usar hashes!
        "role": "admin",
        "name": "Administrador Principal"
    },
    "doctor": {
        "password": "doc123",
        "role": "doctor",
        "name": "Dr. Juan Pérez"
    },
    "reception": {
        "password": "rec123",
        "role": "reception",
        "name": "María Recepción"
    }
}

def login_user(username, password):
    """
    Verifica las credenciales del usuario.
    Retorna el objeto usuario (dict) si es válido, None si no.
    """
    # Simular latencia de red
    time.sleep(0.5)
    
    if username in USERS_DB:
        user_data = USERS_DB[username]
        if user_data["password"] == password:
            return user_data
    
    return None
