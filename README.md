# SeeYouInstagram - Monitor de Instagram

Un programa interactivo de consola en Python para monitorear perfiles de Instagram de forma avanzada.

## 🚀 Características

- **Gestión de Sesiones**: Inicia, guarda, carga y cierra sesiones de Instagram
- **Modo Solo Perfiles Públicos**: Monitorea sin iniciar sesión (solo perfiles públicos)
- **Autenticación 2FA**: Soporte completo para autenticación de dos factores
- **Monitoreo de Perfiles**: Rastrea cambios en seguidores y seguidos
- **Análisis de Conexiones**: Encuentra seguidores mutuos y analiza conexiones internas
- **Persistencia de Datos**: Guarda todos los datos en formato JSON
- **Guardado Parcial**: Recuperación automática en caso de interrupciones
- **Interfaz Colorida**: Interfaz de consola con colores para mejor experiencia

## 📋 Requisitos

- Python 3.7+
- Windows (PowerShell)

## 🛠️ Instalación

1. Clona o descarga el proyecto
2. **IMPORTANTE**: Asegúrate de activar el entorno virtual antes de ejecutar el programa

### Opción 1: Usar scripts de arranque (Recomendado)

**Windows PowerShell:**
```powershell
.\ejecutar.ps1
```

**Windows Command Prompt:**
```cmd
ejecutar.bat
```

### Opción 2: Activación manual

```powershell
# Activar entorno virtual
.\.venv\Scripts\Activate.ps1

# Verificar dependencias
python -c "import colorama, instaloader"

# Ejecutar programa
python main.py
```

**Nota**: Si obtienes el error `ModuleNotFoundError: No module named 'colorama'`, significa que el entorno virtual no está activado correctamente.

## 🎮 Uso

### Inicio Rápido

1. **Ejecuta el programa usando uno de los scripts:**
   ```powershell
   .\ejecutar.ps1    # PowerShell (Recomendado)
   ```
   o
   ```cmd
   ejecutar.bat      # Command Prompt
   ```

2. **O manualmente:**
   ```powershell
   .\.venv\Scripts\Activate.ps1
   python main.py
   ```

### Menú Principal

1. **Gestión de Sesiones**
   - Iniciar sesión con usuario y contraseña
   - Cargar sesión guardada
   - Guardar sesión actual
   - Cerrar sesión

2. **Monitoreo de Perfil**
   - Monitorear cambios en un perfil
   - Ver último reporte generado
   - Limpiar datos de monitoreo

3. **Análisis de Conexiones**
   - Encontrar seguidores mutuos entre dos perfiles
   - Analizar conexiones internas de un perfil

4. **Ver Estado de la Sesión**
   - Mostrar información de la sesión actual

5. **🌐 Modo Solo Perfiles Públicos**
   - Activar monitoreo sin iniciar sesión
   - Solo funciona con perfiles públicos
   - Menor riesgo de detección

## 📁 Estructura de Archivos

```
seeYouInstagram/
├── main.py                 # Archivo principal con interfaz de consola
├── instagram_monitor.py    # Clase principal con todas las funcionalidades
├── utils.py               # Utilidades adicionales y funciones de ayuda
├── config_seguridad.py    # Configuración de seguridad y rate limiting
├── datos_monitoreo/        # Directorio con todos los datos organizados por usuario
│   └── nombre_usuario/     # Carpeta individual para cada usuario monitoreado
│       ├── seguidores/     # Historial de archivos JSON con seguidores
│       │   ├── 2025-08-09_14-30-15_seguidores.json
│       │   ├── 2025-08-09_16-45-22_seguidos_parcial.json  # Archivo temporal
│       │   ├── 2025-08-09_16-45-22_seguidores.json
│       │   └── ...
│       ├── seguidos/       # Historial de archivos JSON con seguidos
│       │   ├── 2025-08-09_14-30-15_seguidos.json
│       │   ├── 2025-08-09_16-45-22_seguidos.json
│       │   └── ...
│       ├── reportes/       # Historial de reportes de cambios
│       │   ├── 2025-08-09_14-30-15_reporte.json
│       │   └── ...
│       └── sesiones/       # Sesiones guardadas
│           └── usuario_session
├── .venv/                 # Entorno virtual de Python
└── README.md              # Este archivo
```

## 🔧 Funcionalidades Detalladas

### Gestión de Sesiones

- **Inicio de Sesión**: Autentica con Instagram usando credenciales
- **2FA**: Soporte automático para código de verificación
- **Persistencia**: Guarda sesiones para uso futuro sin re-autenticación
- **Múltiples Usuarios**: Maneja sesiones de diferentes cuentas

### Monitoreo de Perfiles

- **Primera Ejecución**: Captura estado inicial (seguidores y seguidos)
- **Comparaciones**: Detecta cambios desde el último monitoreo
- **Guardado Parcial**: Guarda automáticamente cada 250 elementos para evitar pérdida de datos
- **Recuperación de Interrupciones**: Continúa desde donde se quedó si el proceso fue interrumpido
- **Historial Completo**: Mantiene todos los archivos JSON con timestamp
- **Organización por Usuario**: Cada usuario tiene su propia carpeta
- **Estructura Separada**: Seguidores y seguidos en carpetas independientes
- **Acceso Automático**: Siempre utiliza los datos más recientes para comparaciones
- **Reportes Detallados**: Muestra:
  - Nuevos seguidores
  - Seguidores perdidos
  - Nuevos seguidos
  - Seguidos eliminados
  - Estadísticas de cambio

### Análisis de Conexiones

- **Seguidores Mutuos**: Encuentra usuarios que siguen a dos perfiles específicos
- **Conexiones Internas**: Identifica seguidores que también son seguidos
- **Ratio de Reciprocidad**: Calcula porcentaje de conexiones mutuas

## ⚠️ Consideraciones Importantes de Seguridad

### 🛡️ Protección contra Detección de Instagram

Instagram tiene sistemas avanzados para detectar actividad automatizada. Este programa incluye varias medidas de seguridad:

- **Delays Aleatorios**: Pausas entre 2-5 segundos entre requests
- **Rate Limiting**: Máximo 15 requests por minuto (muy conservador)
- **Pausas de Seguridad**: Esperas más largas cada 100 elementos procesados
- **Detección de Bloqueos**: Manejo automático de errores de rate limiting
- **Confirmación de Usuario**: Pregunta si continuar en operaciones largas

### 🚨 ¿Qué hacer si Instagram detecta actividad automatizada?

Si recibes un mensaje como "*Creemos que tu cuenta podría estar siendo utilizada por alguien más*":

1. **No te preocupes** - Es normal al usar herramientas de monitoreo
2. **Acepta esperar** cuando el programa te pregunte (recomendado: 10 minutos)
3. **Usa el programa con menos frecuencia** 
4. **Monitorea cuentas más pequeñas** (menos de 1000 seguidores es más seguro)
5. **No uses múltiples herramientas** de Instagram al mismo tiempo

### 📋 Mejores Prácticas

**🌐 Usar Modo Público cuando:**
- ✅ Es tu primera vez usando el programa
- ✅ Solo necesitas monitorear perfiles públicos
- ✅ Quieres máxima seguridad para tu cuenta
- ✅ Prefieres no proporcionar credenciales

**🔐 Usar Modo con Sesión cuando:**
- ✅ Necesitas acceder a perfiles privados
- ✅ Quieres funcionalidad completa
- ✅ Tienes una cuenta dedicada para monitoreo
- ✅ Necesitas análisis más detallados

**⚙️ Configuración General:**
- ✅ **Usa el programa de vez en cuando**, no diariamente
- ✅ **Monitorea pocas cuentas por sesión** (1-2 máximo)
- ✅ **Respeta las pausas** que sugiere el programa
- ✅ **Cierra otras aplicaciones** de Instagram mientras usas esta
- ❌ **No ejecutes múltiples instancias** del programa
- ❌ **No monitorees cuentas enormes** (>10K seguidores) frecuentemente

### ⚙️ Configuración de Seguridad

Puedes personalizar la configuración de seguridad editando `config_seguridad.py`:

```python
# Hacer el programa más conservador (más lento pero más seguro)
MAX_REQUESTS_PER_MINUTE = 10
MIN_DELAY_BETWEEN_REQUESTS = 3.0
MAX_DELAY_BETWEEN_REQUESTS = 8.0

# Hacer el programa más agresivo (más rápido pero más riesgoso)
MAX_REQUESTS_PER_MINUTE = 25
MIN_DELAY_BETWEEN_REQUESTS = 1.0
MAX_DELAY_BETWEEN_REQUESTS = 3.0

# Configurar intervalo de guardado parcial
PARTIAL_SAVE_INTERVAL = 250  # Guarda cada 250 elementos
```

### 🌐 Modo Solo Perfiles Públicos

Una característica única que permite usar el programa sin iniciar sesión:

**¿Cuándo usar este modo?**
- 🔰 **Primera vez usando el programa**
- 🛡️ **Máxima seguridad**: Sin riesgo para tu cuenta personal
- 👁️ **Solo perfiles públicos**: Cuando solo necesitas monitorear cuentas públicas
- 🚫 **Evitar autenticación**: No quieres proporcionar credenciales

**Ventajas:**
- ✅ **Sin riesgo**: No afecta tu cuenta personal de Instagram
- ✅ **Sin detección**: Menor probabilidad de ser detectado como bot
- ✅ **Fácil de usar**: No requiere configuración de sesiones
- ✅ **Rápido**: Acceso inmediato sin autenticación

**Limitaciones:**
- ❌ **Solo perfiles públicos**: No puede acceder a cuentas privadas
- ❌ **Funciones limitadas**: Algunas características pueden no estar disponibles
- ❌ **Rate limiting**: Instagram puede ser más restrictivo

**Ejemplo de uso:**
```
🌐 MODO SOLO PERFILES PÚBLICOS

¿Continuar en modo público? (s/n): s
✅ Modo público activado correctamente

OPCIONES EN MODO PÚBLICO:
1. Monitorear Perfil Público
2. Buscar Seguidores Mutuos  
3. Ver Estado del Modo
4. Desactivar Modo Público
5. Volver al Menú Principal
```

### 💾 Guardado Parcial y Recuperación

El programa incluye un sistema inteligente de guardado parcial:

**¿Cómo funciona?**
- 🔄 **Guardado automático**: Cada 250 elementos obtenidos, se guarda un archivo temporal
- 📁 **Archivos temporales**: Se identifican con `_parcial.json` en el nombre
- 🚀 **Recuperación inteligente**: Si el programa se cierra inesperadamente, detecta archivos parciales
- ✅ **Continuación automática**: Pregunta si quieres continuar desde donde se quedó

**Ejemplo de uso:**
```
📥 Obteniendo seguidores de usuario123...
  Total estimado: 2,500
🔄 Encontrados datos parciales: 750 seguidores
¿Continuar desde donde se quedó? (tienes 750 seguidores guardados) (s/n): s
✅ Continuando desde datos parciales...
  Ya obtenidos: 750
  Restantes: 1,750
💾 Guardado parcial: 1,000 seguidores en 2025-08-09_15-30-22_seguidores_parcial.json
```

**Ventajas:**
- ✅ **Sin pérdida de datos**: Nunca pierdes el progreso por errores de conexión
- ✅ **Flexibilidad**: Puedes pausar y continuar cuando quieras
- ✅ **Eficiencia**: No repites trabajo ya hecho
- ✅ **Limpieza automática**: Los archivos parciales se eliminan al completar

## ⚠️ Otras Consideraciones Importantes

1. **Límites de Instagram**: El programa respeta los límites de la API de Instagram
2. **Sesiones**: Guarda sesiones localmente para evitar múltiples autenticaciones
3. **Privacidad**: Solo accede a información pública de los perfiles
4. **Rendimiento**: Para cuentas con muchos seguidores, el proceso puede ser lento

## 🎨 Características de la Interfaz

- **Menús Numerados**: Navegación fácil con opciones numeradas
- **Colores Descriptivos**: 
  - 🟢 Verde: Éxito y nuevos elementos
  - 🔴 Rojo: Errores y elementos eliminados
  - 🟡 Amarillo: Advertencias e información
  - 🔵 Azul: Información general
  - 🟣 Magenta: Opciones especiales
- **Iconos**: Emojis para identificar rápidamente el tipo de información
- **Progreso**: Indicadores de progreso para operaciones largas

## 🤝 Uso Responsable

Este programa está diseñado para uso personal y educativo. Por favor:

- Respeta los términos de servicio de Instagram
- No uses el programa para spam o acoso
- Considera la privacidad de otros usuarios
- Usa las funcionalidades de manera ética

## 📄 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

---

**Desarrollado con ❤️ para la comunidad**
