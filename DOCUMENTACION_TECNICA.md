# 📋 Documentación Técnica - Nueva Estructura de Datos

## 🔄 Cambios Implementados

### 📁 **Nueva Organización de Archivos**

Anteriormente, los datos se guardaban en archivos individuales por usuario. Ahora se implementó una estructura jerárquica organizada que permite:

#### **Estructura Anterior:**
```
datos_monitoreo/
├── usuario1_datos.json
├── usuario1_reportes.json
├── usuario1_session
├── usuario2_datos.json
└── usuario2_reportes.json
```

#### **Nueva Estructura:**
```
datos_monitoreo/
├── usuario1/
│   ├── seguidores/
│   │   ├── 2025-08-09_14-30-15_seguidores.json
│   │   ├── 2025-08-09_16-45-22_seguidores.json
│   │   └── 2025-08-09_18-12-33_seguidores.json
│   ├── seguidos/
│   │   ├── 2025-08-09_14-30-15_seguidos.json
│   │   ├── 2025-08-09_16-45-22_seguidos.json
│   │   └── 2025-08-09_18-12-33_seguidos.json
│   ├── reportes/
│   │   ├── 2025-08-09_14-30-15_reporte.json
│   │   └── 2025-08-09_16-45-22_reporte.json
│   └── sesiones/
│       └── usuario1_session
└── usuario2/
    ├── seguidores/
    ├── seguidos/
    ├── reportes/
    └── sesiones/
```

## 🎯 **Ventajas de la Nueva Estructura**

### 1. **Historial Completo**
- **Problema anterior**: Solo se mantenía el estado actual y el anterior
- **Solución actual**: Se mantiene un historial completo de todos los monitoreos
- **Beneficio**: Permite análisis temporal y recuperación de datos históricos

### 2. **Organización por Usuario**
- **Problema anterior**: Archivos mezclados en un solo directorio
- **Solución actual**: Cada usuario tiene su propia carpeta
- **Beneficio**: Fácil navegación y mantenimiento de datos

### 3. **Separación de Tipos de Datos**
- **Problema anterior**: Seguidores y seguidos en el mismo archivo
- **Solución actual**: Carpetas separadas para cada tipo de datos
- **Beneficio**: Acceso granular y mejor organización

### 4. **Timestamps Descriptivos**
- **Problema anterior**: Solo fecha de modificación del archivo
- **Solución actual**: Timestamp en el nombre del archivo
- **Beneficio**: Identificación rápida de cuándo se generó cada archivo

## 🔧 **Funciones Técnicas Implementadas**

### `crear_estructura_usuario(username)`
```python
def crear_estructura_usuario(self, username: str) -> Dict[str, str]:
    """Crea la estructura completa de carpetas para un usuario"""
    # Crea: usuario/seguidores/, usuario/seguidos/, usuario/reportes/, usuario/sesiones/
    return dict_con_rutas_creadas
```

### `generar_timestamp()`
```python
def generar_timestamp(self) -> str:
    """Genera timestamp en formato: YYYY-MM-DD_HH-MM-SS"""
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
```

### `obtener_archivo_mas_reciente(carpeta, tipo)`
```python
def obtener_archivo_mas_reciente(self, carpeta: str, tipo: str) -> Optional[str]:
    """Obtiene el archivo más reciente basado en fecha de modificación"""
    # Automáticamente selecciona el archivo más nuevo para comparaciones
    return ruta_archivo_mas_reciente
```

### `guardar_datos_actuales(username, seguidores, seguidos)`
```python
def guardar_datos_actuales(self, username: str, seguidores: Set[str], seguidos: Set[str]) -> None:
    """Guarda datos en archivos separados con timestamp único"""
    # Crea: timestamp_seguidores.json y timestamp_seguidos.json
```

## 📊 **Formato de Archivos JSON**

### **Archivo de Seguidores** (`YYYY-MM-DD_HH-MM-SS_seguidores.json`)
```json
{
  "username": "usuario_monitoreado",
  "fecha_actualizacion": "2025-08-09T14:30:15.123456",
  "timestamp": "2025-08-09_14-30-15",
  "seguidores": ["usuario1", "usuario2", "usuario3"],
  "total_seguidores": 3,
  "tipo": "seguidores"
}
```

### **Archivo de Seguidos** (`YYYY-MM-DD_HH-MM-SS_seguidos.json`)
```json
{
  "username": "usuario_monitoreado",
  "fecha_actualizacion": "2025-08-09T14:30:15.123456",
  "timestamp": "2025-08-09_14-30-15",
  "seguidos": ["seguido1", "seguido2"],
  "total_seguidos": 2,
  "tipo": "seguidos"
}
```

### **Archivo de Reporte** (`YYYY-MM-DD_HH-MM-SS_reporte.json`)
```json
{
  "es_primer_monitoreo": false,
  "username": "usuario_monitoreado",
  "fecha_anterior": "2025-08-09T14:30:15.123456",
  "fecha_actual": "2025-08-09T16:45:22.654321",
  "timestamp": "2025-08-09_16-45-22",
  "cambios_seguidores": {
    "nuevos": ["nuevo_seguidor1"],
    "perdidos": ["seguidor_perdido1"],
    "total_nuevos": 1,
    "total_perdidos": 1
  },
  "cambios_seguidos": {
    "nuevos": ["nuevo_seguido1"],
    "eliminados": ["seguido_eliminado1"],
    "total_nuevos": 1,
    "total_eliminados": 1
  },
  "estadisticas": {
    "seguidores_anteriores": 100,
    "seguidores_actuales": 100,
    "seguidos_anteriores": 50,
    "seguidos_actuales": 50,
    "cambio_neto_seguidores": 0,
    "cambio_neto_seguidos": 0
  }
}
```

## 🔄 **Flujo de Trabajo**

### **Primer Monitoreo:**
1. Se crea la estructura de carpetas para el usuario
2. Se obtienen seguidores y seguidos actuales
3. Se guardan en archivos con timestamp
4. Se muestra mensaje de primer monitoreo

### **Monitoreos Posteriores:**
1. Se cargan los datos más recientes (usando `obtener_archivo_mas_reciente()`)
2. Se obtienen los datos actuales
3. Se comparan para generar el reporte de cambios
4. Se guardan los nuevos datos con nuevo timestamp
5. Se guarda el reporte con el mismo timestamp

### **Acceso a Datos Históricos:**
- Los datos anteriores siguen disponibles en sus respectivos archivos
- El programa siempre usa automáticamente los más recientes para comparaciones
- El usuario puede acceder manualmente a cualquier archivo histórico

## 🎨 **Nueva Funcionalidad de UI**

### **Menú de Monitoreo Actualizado:**
```
MONITOREO DE PERFIL:
1. Iniciar Monitoreo de Perfil
2. Ver Último Reporte
3. Ver Estructura de Archivos    ← NUEVO
4. Limpiar Datos de Monitoreo
5. Volver al Menú Principal
```

### **Función `mostrar_estructura_archivos()`:**
- Lista todos los usuarios monitoreados
- Muestra cantidad de archivos por tipo
- Muestra los timestamps de los archivos más recientes
- Proporciona una vista general de todos los datos almacenados

## 📈 **Beneficios para el Usuario**

1. **Historial Completo**: Nunca pierdes datos históricos
2. **Mejor Organización**: Fácil navegación entre usuarios y tipos de datos
3. **Análisis Temporal**: Posibilidad de analizar tendencias a lo largo del tiempo
4. **Backup Natural**: Los datos anteriores actúan como backup automático
5. **Escalabilidad**: La estructura soporta múltiples usuarios eficientemente
6. **Transparencia**: Fácil acceso a cualquier dato específico por fecha

## 🛠️ **Mantenimiento y Limpieza**

- La función `limpiar_datos_monitoreo()` elimina toda la estructura
- Cada archivo es independiente, permitiendo limpieza selectiva manual
- Los archivos antiguos pueden eliminarse manualmente si se desea liberar espacio
- El programa siempre funciona correctamente independientemente de la cantidad de archivos históricos

---

**Esta nueva estructura mantiene la compatibilidad funcional mientras añade robustez y flexibilidad al sistema de monitoreo.**
