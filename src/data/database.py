import sqlite3
import pandas as pd
from datetime import datetime

DB_NAME = "dental_guard.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def init_db():
    """Inicializa la base de datos creando las tablas si no existen."""
    conn = get_connection()
    c = conn.cursor()
    
    # Tabla Pacientes
    c.execute('''
        CREATE TABLE IF NOT EXISTS pacientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            edad INTEGER,
            historial TEXT,
            fecha_registro DATE
        )
    ''')
    
    # Tabla Citas
    c.execute('''
        CREATE TABLE IF NOT EXISTS citas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            paciente_id INTEGER,
            fecha TEXT,
            motivo TEXT,
            FOREIGN KEY (paciente_id) REFERENCES pacientes (id)
        )
    ''')
    
    # Tabla Imagenes
    c.execute('''
        CREATE TABLE IF NOT EXISTS imagenes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            paciente_id INTEGER,
            ruta_archivo TEXT,
            fecha TEXT,
            tipo TEXT,
            FOREIGN KEY (paciente_id) REFERENCES pacientes (id)
        )
    ''')
    
    conn.commit()
    conn.close()

# --- CRUD Pacientes ---

def add_paciente(nombre, edad, historial):
    conn = get_connection()
    c = conn.cursor()
    fecha_registro = datetime.now().strftime("%Y-%m-%d")
    c.execute("INSERT INTO pacientes (nombre, edad, historial, fecha_registro) VALUES (?, ?, ?, ?)",
              (nombre, edad, historial, fecha_registro))
    conn.commit()
    conn.close()

def get_pacientes():
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM pacientes", conn)
    conn.close()
    return df

# --- CRUD Citas ---

def add_cita(paciente_id, fecha, motivo):
    conn = get_connection()
    c = conn.cursor()
    c.execute("INSERT INTO citas (paciente_id, fecha, motivo) VALUES (?, ?, ?)",
              (paciente_id, fecha, motivo))
    conn.commit()
    conn.close()

def get_citas():
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM citas", conn)
    conn.close()
    return df

# --- CRUD Imagenes ---

def add_imagen(paciente_id, ruta_archivo, tipo):
    conn = get_connection()
    c = conn.cursor()
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("INSERT INTO imagenes (paciente_id, ruta_archivo, fecha, tipo) VALUES (?, ?, ?, ?)",
              (paciente_id, ruta_archivo, fecha, tipo))
    conn.commit()
    conn.close()

def get_imagenes(paciente_id):
    conn = get_connection()
    # Usamos parámetros para evitar SQL Injection, pero pandas read_sql_query con params es lo ideal
    df = pd.read_sql_query("SELECT * FROM imagenes WHERE paciente_id = ?", conn, params=(paciente_id,))
    conn.close()
    return df
