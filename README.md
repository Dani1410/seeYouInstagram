# SeeYouInstagram - Monitor de Instagram

Un programa interactivo de consola en Python para monitorear perfiles de Instagram de forma avanzada.

## 🚀 Características

- **Gestión de Sesiones**: Inicia, guarda, carga y cierra sesiones de Instagram
- **Autenticación 2FA**: Soporte completo para autenticación de dos factores
- **Monitoreo de Perfiles**: Rastrea cambios en seguidores y seguidos
- **Análisis de Conexiones**: Encuentra seguidores mutuos y analiza conexiones internas
- **Persistencia de Datos**: Guarda todos los datos en formato JSON
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

## 📁 Estructura de Archivos

```
seeYouInstagram/
├── main.py                 # Archivo principal con interfaz de consola
├── instagram_monitor.py    # Clase principal con todas las funcionalidades
├── utils.py               # Utilidades adicionales y funciones de ayuda
├── config.py              # Archivo de configuración personalizable
├── guia_uso.py           # Guía de uso rápido con ejemplos
├── datos_monitoreo/        # Directorio con todos los datos organizados por usuario
│   └── nombre_usuario/     # Carpeta individual para cada usuario monitoreado
│       ├── seguidores/     # Historial de archivos JSON con seguidores
│       │   ├── 2025-08-09_14-30-15_seguidores.json
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

## ⚠️ Consideraciones Importantes

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
