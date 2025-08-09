#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuración de Seguridad para SeeYouInstagram
Ajusta estos valores para controlar qué tan conservador es el programa
"""

# ========================================
# CONFIGURACIÓN DE RATE LIMITING
# ========================================

# Máximo número de requests por minuto (muy conservador por defecto)
MAX_REQUESTS_PER_MINUTE = 15

# Delay mínimo y máximo entre requests (en segundos)
MIN_DELAY_BETWEEN_REQUESTS = 2.0
MAX_DELAY_BETWEEN_REQUESTS = 5.0

# Delay extra cada ciertos elementos procesados
ELEMENTS_BEFORE_LONG_PAUSE = 100
LONG_PAUSE_MIN = 3.0
LONG_PAUSE_MAX = 7.0

# ========================================
# CONFIGURACIÓN DE MODO PÚBLICO
# ========================================

# Habilitar modo solo perfiles públicos (sin iniciar sesión)
ENABLE_PUBLIC_MODE = True

# Mensaje de advertencia para modo público
PUBLIC_MODE_WARNING = """
🌐 MODO SOLO PERFILES PÚBLICOS ACTIVADO

VENTAJAS:
✅ No requiere iniciar sesión en Instagram
✅ Menor riesgo de detección de automatización
✅ No afecta tu cuenta personal de Instagram
✅ Ideal para monitorear cuentas públicas

LIMITACIONES:
❌ Solo funciona con perfiles públicos
❌ No puede acceder a perfiles privados
❌ Algunas funciones pueden estar limitadas
❌ Instagram puede ser más restrictivo sin autenticación

¿Continuar en modo público?
"""

# ========================================
# CONFIGURACIÓN DE ADVERTENCIAS
# ========================================

# Cada cuántos elementos preguntar al usuario si continuar
ASK_USER_EVERY_N_ELEMENTS = 25

# Límite de seguidores para mostrar advertencia de tiempo
WARNING_FOLLOWERS_LIMIT = 500

# Límite de seguidos para mostrar advertencia de tiempo
WARNING_FOLLOWING_LIMIT = 450

# ========================================
# CONFIGURACIÓN DE TIMEOUTS
# ========================================

# Tiempo de espera cuando Instagram bloquea (en segundos)
RATE_LIMIT_WAIT_TIME = 600  # 10 minutos

# Timeout para conexiones (en segundos)
CONNECTION_TIMEOUT = 300    # 5 minutos

# Máximo número de intentos de conexión
MAX_CONNECTION_ATTEMPTS = 3

# ========================================
# CONFIGURACIÓN DE MONITOREO
# ========================================

# Mostrar progreso cada N elementos
PROGRESS_UPDATE_INTERVAL = 20

# Guardar datos parciales cada N elementos (para recuperación en caso de error)
PARTIAL_SAVE_INTERVAL = 60

# Preguntar al usuario si continuar cada N elementos
ASK_USER_CONTINUE_INTERVAL = 120

# Pausa de seguridad cada N elementos
SECURITY_PAUSE_INTERVAL = 180

# ========================================
# MENSAJES DE SEGURIDAD
# ========================================

RATE_LIMIT_MESSAGE = """
⚠️  IMPORTANTE: Instagram ha detectado actividad automatizada

Esto es completamente normal al usar herramientas de monitoreo como esta.
Instagram tiene sistemas para detectar bots y proteger su plataforma.

Recomendaciones:
• Espera unos minutos antes de continuar
• Usa el programa con menos frecuencia
• Considera monitorear cuentas más pequeñas
• No uses múltiples herramientas de Instagram simultáneamente

¿Quieres esperar y continuar automáticamente?
"""

SAFETY_REMINDER = """
💡 RECORDATORIO DE SEGURIDAD:

• Este programa respeta los límites de Instagram
• Usa delays aleatorios para parecer más humano
• Se detiene automáticamente si detecta problemas
• Siempre puedes cancelar con Ctrl+C

Para uso más seguro:
• No monitorees muchas cuentas seguidas
• Usa el programa solo cuando sea necesario
• Respeta la privacidad de otros usuarios
"""

# ========================================
# CONFIGURACIÓN AVANZADA (Solo usuarios expertos)
# ========================================

# User Agent personalizado (deja None para usar el por defecto)
CUSTOM_USER_AGENT = None

# Headers adicionales para las requests
CUSTOM_HEADERS = {}

# Activar modo debug (muestra más información técnica)
DEBUG_MODE = False

# Activar logging detallado
ENABLE_DETAILED_LOGGING = False
