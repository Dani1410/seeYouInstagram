#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Archivo de configuración para el Monitor de Instagram
Puedes modificar estos valores según tus necesidades
"""

# Configuración de archivos y directorios
DIRECTORIO_DATOS = "datos_monitoreo"
EXTENSION_DATOS = "_datos.json"
EXTENSION_REPORTES = "_reportes.json"
EXTENSION_SESION = "_session"

# Configuración de la interfaz
USAR_COLORES = True
MOSTRAR_ICONOS = True

# Configuración de monitoreo
MAX_REPORTES_GUARDADOS = 50
MAX_USUARIOS_MOSTRAR = 10  # Máximo de usuarios a mostrar en listas largas

# Configuración de timeouts
TIMEOUT_CONEXION = 30  # segundos
REINTENTOS_CONEXION = 3

# Configuración de seguridad
GUARDAR_SESIONES = True  # Cambiar a False para no guardar sesiones
LIMPIAR_SESIONES_AL_SALIR = False  # Cambiar a True para limpiar sesiones automáticamente

# Mensajes personalizados
MENSAJE_BIENVENIDA = "Bienvenido al Monitor de Instagram SeeYouInstagram"
MENSAJE_DESPEDIDA = "¡Gracias por usar SeeYouInstagram! 👋"

# Configuración de logs (para futuras versiones)
HABILITAR_LOGS = False
NIVEL_LOG = "INFO"  # DEBUG, INFO, WARNING, ERROR
ARCHIVO_LOG = "seeyouinstagram.log"
