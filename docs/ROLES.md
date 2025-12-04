# Roles y Permisos - DentalGuard ERP

Este documento define los roles de usuario y sus niveles de acceso dentro del sistema.

## Roles Definidos

### 1. Admin (`admin`)
*   **Descripción**: Administrador del sistema con acceso total.
*   **Permisos**:
    *   Gestión de usuarios (crear, editar, eliminar).
    *   Configuración del sistema.
    *   Acceso a todos los reportes y estadísticas.
    *   Gestión de base de datos.

### 2. Doctor (`doctor`)
*   **Descripción**: Odontólogo o especialista médico.
*   **Permisos**:
    *   Ver y editar historias clínicas de pacientes.
    *   Gestionar su propia agenda de citas.
    *   Registrar tratamientos y evoluciones.
    *   Ver reportes de sus pacientes.

### 3. Recepción (`reception`) [Planificado]
*   **Descripción**: Personal encargado de la atención al cliente y agenda.
*   **Permisos**:
    *   Gestión de citas (agendar, cancelar, reprogramar).
    *   Registro básico de pacientes.
    *   Facturación y cobros.

## Matriz de Acceso (MVP)

| Módulo | Admin | Doctor | Recepción |
| :--- | :---: | :---: | :---: |
| Login | ✅ | ✅ | ✅ |
| Dashboard Admin | ✅ | ❌ | ❌ |
| Agenda | ✅ | ✅ | ✅ |
| Pacientes | ✅ | ✅ | ✅ |
| Configuración | ✅ | ❌ | ❌ |
