# 🛠️ Solución de Problemas - SeeYouInstagram

## ❌ Errores Comunes y Soluciones

### 1. `ModuleNotFoundError: No module named 'colorama'`

**Problema**: El entorno virtual no está activado correctamente.

**Solución**:
```powershell
# Activar entorno virtual
.\.venv\Scripts\Activate.ps1

# Verificar que esté activado (debería mostrar (.venv) al inicio del prompt)
# Ejecutar el programa
python main.py
```

**Solución alternativa**:
```powershell
# Usar script de arranque automático
.\ejecutar.ps1
```

### 2. `cannot import name 'InstagramMonitor'`

**Problema**: Error en el archivo `instagram_monitor.py`.

**Solución**:
```powershell
# Verificar que el archivo existe y es válido
python -c "from instagram_monitor import InstagramMonitor; print('✅ Importación exitosa')"
```

### 3. `execution of scripts is disabled`

**Problema**: PowerShell no permite ejecutar scripts.

**Solución**:
```powershell
# Permitir ejecución de scripts para el usuario actual
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force

# Luego ejecutar el script
.\ejecutar.ps1
```

### 4. Problemas de Conexión con Instagram

**Problema**: `ConnectionError` o timeouts.

**Soluciones**:
- Verificar conexión a internet
- Esperar unos minutos y reintentar
- Instagram puede tener límites de velocidad

### 5. Error de Autenticación

**Problema**: `BadCredentialsException`.

**Soluciones**:
- Verificar usuario y contraseña
- Si tienes 2FA activado, asegúrate de ingresar el código correcto
- Cerrar sesión y volver a iniciar

### 6. El programa se cierra inesperadamente

**Problema**: Error no controlado.

**Solución**:
```powershell
# Ejecutar con información de debug
python main.py
# Si hay error, aparecerá el traceback completo
```

### 7. Problema con la estructura de carpetas

**Problema**: No se crean las carpetas correctamente.

**Solución**:
```powershell
# Verificar permisos de escritura en el directorio
# Verificar que el usuario tenga permisos para crear carpetas
```

## 📋 Verificación del Sistema

### Verificar Entorno Virtual
```powershell
# Debe mostrar (.venv) al inicio
.\.venv\Scripts\Activate.ps1
```

### Verificar Dependencias
```powershell
python -c "import colorama, instaloader; print('✅ Todas las dependencias OK')"
```

### Verificar Estructura del Proyecto
```powershell
# Estos archivos deben existir:
ls main.py, instagram_monitor.py, requirements.txt
```

### Verificar Permisos
```powershell
# Crear carpeta de prueba
mkdir test_permisos
rmdir test_permisos
```

## 🚀 Reinstalación Completa

Si nada funciona, reinstalar desde cero:

```powershell
# 1. Eliminar entorno virtual existente
rmdir .venv -Recurse -Force

# 2. Crear nuevo entorno virtual
python -m venv .venv

# 3. Activar entorno virtual
.\.venv\Scripts\Activate.ps1

# 4. Instalar dependencias
pip install -r requirements.txt

# 5. Verificar instalación
python -c "import colorama, instaloader; print('✅ Reinstalación exitosa')"

# 6. Ejecutar programa
python main.py
```

## 📞 Información de Soporte

Si continúas teniendo problemas:

1. **Verifica la versión de Python**: `python --version` (debe ser 3.7+)
2. **Verifica el sistema operativo**: Windows 10/11
3. **Verifica PowerShell**: `$PSVersionTable.PSVersion` (debe ser 5.1+)

## 🔍 Logs y Debugging

Para obtener más información sobre errores:

```powershell
# Ejecutar con verbose
python -v main.py

# O capturar errores en archivo
python main.py 2> errores.log
```

---

**Recuerda**: La mayoría de problemas se resuelven asegurándose de que el entorno virtual esté activado correctamente antes de ejecutar el programa.
