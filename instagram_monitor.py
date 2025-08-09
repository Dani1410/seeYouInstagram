#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Módulo principal para el monitoreo de Instagram
Contiene la clase InstagramMonitor con todas las funcionalidades
"""

import json
import os
import pickle
import time
import random
from datetime import datetime
from typing import Set, Dict, List, Optional
import instaloader
from colorama import Fore, Style
from utils import (
    formatear_fecha, validar_username, limpiar_username, 
    mostrar_barra_progreso, confirmar_accion, formatear_numero,
    truncar_lista, obtener_emoji_cambio
)

class InstagramMonitor:
    """Clase principal para el monitoreo de Instagram"""
    
    def __init__(self):
        """Inicializa el monitor de Instagram con configuración conservadora"""
        # Configurar instaloader con delays para evitar detección
        self.loader = instaloader.Instaloader(
            download_pictures=False,
            download_videos=False,
            download_video_thumbnails=False,
            download_geotags=False,
            download_comments=False,
            save_metadata=False,
            compress_json=False,
            post_metadata_txt_pattern="",
            storyitem_metadata_txt_pattern="",
            max_connection_attempts=3,
            request_timeout=300
        )
        
        self.sesion_activa = False
        self.username_actual = None
        self.modo_publico = False  # Nuevo: modo solo perfiles públicos
        
        # Contadores para manejo conservador de requests
        self.requests_count = 0
        self.last_request_time = time.time()
        self.MAX_REQUESTS_PER_MINUTE = 15  # Muy conservador
        
        # Crear directorio de datos si no existe
        self.directorio_datos = "datos_monitoreo"
        if not os.path.exists(self.directorio_datos):
            os.makedirs(self.directorio_datos)
    
    def _wait_if_needed(self):
        """
        Implementa delays inteligentes para evitar detección de automatización
        """
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        # Si han pasado más de 60 segundos, resetear contador
        if time_since_last > 60:
            self.requests_count = 0
        
        # Si hemos hecho muchos requests recientemente, esperar más
        if self.requests_count >= self.MAX_REQUESTS_PER_MINUTE:
            wait_time = 60 - time_since_last
            if wait_time > 0:
                print(f"{Fore.YELLOW}⏳ Esperando {int(wait_time)} segundos para respetar límites de Instagram...{Style.RESET_ALL}")
                time.sleep(wait_time)
                self.requests_count = 0
        
        # Delay aleatorio entre requests (2-5 segundos)
        delay = random.uniform(2.0, 5.0)
        time.sleep(delay)
        
        self.requests_count += 1
        self.last_request_time = time.time()
    
    def _handle_rate_limit_error(self, error_msg: str) -> bool:
        """
        Maneja errores de rate limiting de Instagram
        
        Args:
            error_msg: Mensaje de error
            
        Returns:
            bool: True si se debe reintentar, False si es un error permanente
        """
        if "Please wait" in error_msg or "Try again later" in error_msg or "rate limit" in error_msg.lower():
            print(f"{Fore.YELLOW}⚠️ Instagram ha detectado actividad automatizada{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}💡 Esto es normal al usar herramientas de monitoreo{Style.RESET_ALL}")
            
            if confirmar_accion("¿Esperar 10 minutos y continuar? (recomendado)"):
                print(f"{Fore.CYAN}⏳ Esperando 10 minutos para respetar los límites de Instagram...{Style.RESET_ALL}")
                for i in range(600, 0, -30):  # 10 minutos en bloques de 30 segundos
                    mins, secs = divmod(i, 60)
                    print(f"\r{Fore.CYAN}⏳ Tiempo restante: {mins:02d}:{secs:02d}{Style.RESET_ALL}", end="", flush=True)
                    time.sleep(30)
                print(f"\n{Fore.GREEN}✅ Listo para continuar{Style.RESET_ALL}")
                return True
            else:
                print(f"{Fore.YELLOW}⚠️ Operación cancelada por el usuario{Style.RESET_ALL}")
                return False
        
        return False
    
    def _guardar_datos_parciales(self, username: str, datos: Set[str], tipo: str, timestamp: str):
        """
        Guarda datos parciales durante el proceso de obtención para evitar pérdidas
        
        Args:
            username: Nombre de usuario
            datos: Conjunto de datos a guardar
            tipo: Tipo de datos ('seguidores' o 'seguidos')
            timestamp: Timestamp para el nombre del archivo
        """
        try:
            carpetas = self.crear_estructura_usuario(username)
            carpeta_tipo = carpetas[tipo]
            
            # Crear archivo temporal con sufijo _parcial
            nombre_archivo = f"{timestamp}_{tipo}_parcial.json"
            ruta_archivo = os.path.join(carpeta_tipo, nombre_archivo)
            
            datos_json = {
                "usuario": username,
                "tipo": tipo,
                "timestamp": timestamp,
                "fecha_obtencion": formatear_fecha(datetime.now()),
                "total_obtenidos": len(datos),
                "status": "parcial",
                "datos": list(datos)
            }
            
            with open(ruta_archivo, 'w', encoding='utf-8') as f:
                json.dump(datos_json, f, indent=2, ensure_ascii=False)
            
            print(f"{Fore.CYAN}💾 Guardado parcial: {len(datos)} {tipo} en {nombre_archivo}{Style.RESET_ALL}")
            
        except Exception as e:
            print(f"{Fore.YELLOW}⚠️ No se pudo guardar datos parciales: {str(e)}{Style.RESET_ALL}")
    
    def _finalizar_archivo_parcial(self, username: str, datos: Set[str], tipo: str, timestamp: str):
        """
        Convierte un archivo parcial en el archivo final y elimina el parcial
        
        Args:
            username: Nombre de usuario
            datos: Conjunto completo de datos
            tipo: Tipo de datos ('seguidores' o 'seguidos')
            timestamp: Timestamp para el nombre del archivo
        """
        try:
            carpetas = self.crear_estructura_usuario(username)
            carpeta_tipo = carpetas[tipo]
            
            # Nombres de archivos
            archivo_parcial = f"{timestamp}_{tipo}_parcial.json"
            archivo_final = f"{timestamp}_{tipo}.json"
            ruta_parcial = os.path.join(carpeta_tipo, archivo_parcial)
            ruta_final = os.path.join(carpeta_tipo, archivo_final)
            
            # Crear archivo final
            datos_json = {
                "usuario": username,
                "tipo": tipo,
                "timestamp": timestamp,
                "fecha_obtencion": formatear_fecha(datetime.now()),
                "total": len(datos),
                "status": "completo",
                "datos": list(datos)
            }
            
            with open(ruta_final, 'w', encoding='utf-8') as f:
                json.dump(datos_json, f, indent=2, ensure_ascii=False)
            
            # Eliminar archivo parcial si existe
            if os.path.exists(ruta_parcial):
                os.remove(ruta_parcial)
                print(f"{Fore.GREEN}✅ Archivo final guardado: {archivo_final} (parcial eliminado){Style.RESET_ALL}")
            else:
                print(f"{Fore.GREEN}✅ Archivo final guardado: {archivo_final}{Style.RESET_ALL}")
            
        except Exception as e:
            print(f"{Fore.YELLOW}⚠️ Error al finalizar archivo: {str(e)}{Style.RESET_ALL}")
    
    def _recuperar_datos_parciales(self, username: str, tipo: str) -> Optional[tuple]:
        """
        Recupera datos de un archivo parcial existente si hay uno
        
        Args:
            username: Nombre de usuario
            tipo: Tipo de datos ('seguidores' o 'seguidos')
            
        Returns:
            Tuple (datos_recuperados, timestamp) o None si no hay archivo parcial
        """
        try:
            carpetas = self.crear_estructura_usuario(username)
            carpeta_tipo = carpetas[tipo]
            
            if not os.path.exists(carpeta_tipo):
                return None
            
            # Buscar archivos parciales
            archivos_parciales = [f for f in os.listdir(carpeta_tipo) if f.endswith(f'_{tipo}_parcial.json')]
            
            if not archivos_parciales:
                return None
            
            # Tomar el más reciente
            archivo_mas_reciente = sorted(archivos_parciales)[-1]
            ruta_archivo = os.path.join(carpeta_tipo, archivo_mas_reciente)
            
            with open(ruta_archivo, 'r', encoding='utf-8') as f:
                datos_json = json.load(f)
            
            datos_recuperados = set(datos_json.get('datos', []))
            timestamp = datos_json.get('timestamp', '')
            total_recuperados = len(datos_recuperados)
            
            if total_recuperados > 0:
                print(f"{Fore.YELLOW}🔄 Encontrados datos parciales: {total_recuperados} {tipo}{Style.RESET_ALL}")
                if confirmar_accion(f"¿Continuar desde donde se quedó? (tienes {total_recuperados} {tipo} guardados)"):
                    print(f"{Fore.GREEN}✅ Continuando desde datos parciales...{Style.RESET_ALL}")
                    return (datos_recuperados, timestamp)
                else:
                    # Eliminar archivo parcial si no se quiere continuar
                    os.remove(ruta_archivo)
                    print(f"{Fore.YELLOW}🗑️ Archivo parcial eliminado, empezando desde cero{Style.RESET_ALL}")
            
            return None
            
        except Exception as e:
            print(f"{Fore.YELLOW}⚠️ Error al recuperar datos parciales: {str(e)}{Style.RESET_ALL}")
            return None
    
    def activar_modo_publico(self) -> bool:
        """
        Activa el modo de solo perfiles públicos (sin iniciar sesión)
        
        Returns:
            bool: True si se activó correctamente
        """
        try:
            print(f"{Fore.CYAN}🌐 Activando modo solo perfiles públicos...{Style.RESET_ALL}")
            
            # Mostrar advertencia sobre limitaciones
            print(f"{Fore.YELLOW}⚠️ MODO SOLO PERFILES PÚBLICOS{Style.RESET_ALL}")
            print(f"{Fore.GREEN}✅ Ventajas:{Style.RESET_ALL}")
            print(f"  • No requiere iniciar sesión")
            print(f"  • Menor riesgo de detección")
            print(f"  • No afecta tu cuenta personal")
            print(f"  • Ideal para perfiles públicos")
            
            print(f"\n{Fore.YELLOW}⚠️ Limitaciones:{Style.RESET_ALL}")
            print(f"  • Solo funciona con perfiles públicos")
            print(f"  • No puede acceder a perfiles privados")
            print(f"  • No puede obtener listas de seguidores/seguidos")
            print(f"  • Solo puede ver información básica del perfil")
            print(f"  • Funcionalidad limitada por restricciones de Instagram")
            
            if confirmar_accion("¿Continuar en modo público?"):
                self.modo_publico = True
                self.sesion_activa = False  # No hay sesión real
                self.username_actual = "modo_publico"
                
                print(f"{Fore.GREEN}✅ Modo público activado correctamente{Style.RESET_ALL}")
                print(f"{Fore.CYAN}💡 Ahora puedes monitorear perfiles públicos sin iniciar sesión{Style.RESET_ALL}")
                return True
            else:
                print(f"{Fore.YELLOW}⚠️ Modo público cancelado{Style.RESET_ALL}")
                return False
                
        except Exception as e:
            print(f"{Fore.RED}❌ Error al activar modo público: {str(e)}{Style.RESET_ALL}")
            return False
    
    def esta_en_modo_publico(self) -> bool:
        """
        Verifica si está en modo público
        
        Returns:
            bool: True si está en modo público
        """
        return self.modo_publico
    
    def puede_acceder_perfil(self, username: str) -> bool:
        """
        Verifica si puede acceder a un perfil según el modo actual
        
        Args:
            username: Nombre de usuario a verificar
            
        Returns:
            bool: True si puede acceder al perfil
        """
        try:
            if self.modo_publico:
                # En modo público, verificar que el perfil sea público
                profile = instaloader.Profile.from_username(self.loader.context, username)
                if profile.is_private:
                    print(f"{Fore.RED}❌ El perfil '{username}' es privado y estás en modo público{Style.RESET_ALL}")
                    print(f"{Fore.YELLOW}💡 Para acceder a perfiles privados necesitas iniciar sesión{Style.RESET_ALL}")
                    return False
                return True
            else:
                # En modo con sesión, verificar autenticación
                return self.sesion_activa
                
        except instaloader.exceptions.ProfileNotExistsException:
            print(f"{Fore.RED}❌ El perfil '{username}' no existe{Style.RESET_ALL}")
            return False
        except Exception as e:
            print(f"{Fore.RED}❌ Error al verificar perfil: {str(e)}{Style.RESET_ALL}")
            return False

    def obtener_info_perfil_publico(self, username: str) -> None:
        """
        Obtiene información básica de un perfil público (funciona sin autenticación)
        
        Args:
            username: Nombre de usuario a analizar
        """
        try:
            username = limpiar_username(username)
            if not validar_username(username):
                print(f"{Fore.RED}❌ Nombre de usuario inválido: {username}{Style.RESET_ALL}")
                return
                
            print(f"{Fore.CYAN}📋 Obteniendo información de @{username}...{Style.RESET_ALL}")
            
            # Obtener el perfil sin autenticación
            profile = instaloader.Profile.from_username(self.loader.context, username)
            
            print(f"\n{Fore.CYAN}{'='*50}")
            print(f"📊 INFORMACIÓN DEL PERFIL: @{username}")
            print(f"{'='*50}{Style.RESET_ALL}")
            
            print(f"\n{Fore.GREEN}👤 Información básica:{Style.RESET_ALL}")
            print(f"  • Nombre completo: {profile.full_name}")
            print(f"  • Nombre de usuario: @{profile.username}")
            print(f"  • Es privado: {'Sí' if profile.is_private else 'No'}")
            print(f"  • Es verificado: {'Sí' if profile.is_verified else 'No'}")
            print(f"  • Es cuenta de negocio: {'Sí' if profile.is_business_account else 'No'}")
            
            print(f"\n{Fore.BLUE}📊 Estadísticas:{Style.RESET_ALL}")
            print(f"  • Publicaciones: {formatear_numero(profile.mediacount)}")
            print(f"  • Seguidores: {formatear_numero(profile.followers)}")
            print(f"  • Seguidos: {formatear_numero(profile.followees)}")
            
            if profile.biography:
                print(f"\n{Fore.MAGENTA}📝 Biografía:{Style.RESET_ALL}")
                print(f"  {profile.biography}")
            
            if profile.external_url:
                print(f"\n{Fore.CYAN}🔗 URL externa:{Style.RESET_ALL}")
                print(f"  {profile.external_url}")
                
            if profile.is_private:
                print(f"\n{Fore.YELLOW}🔒 Este perfil es privado - información limitada disponible{Style.RESET_ALL}")
                if self.modo_publico:
                    print(f"{Fore.YELLOW}💡 Para acceder a más información, inicia sesión desde el menú principal{Style.RESET_ALL}")
            else:
                print(f"\n{Fore.GREEN}🔓 Este perfil es público - información completa disponible{Style.RESET_ALL}")
                if self.modo_publico:
                    print(f"{Fore.YELLOW}💡 Para obtener listas de seguidores/seguidos, inicia sesión desde el menú principal{Style.RESET_ALL}")
            
            print(f"\n{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
            
        except instaloader.exceptions.ProfileNotExistsException:
            print(f"{Fore.RED}❌ El perfil '@{username}' no existe{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}❌ Error al obtener información del perfil: {str(e)}{Style.RESET_ALL}")
            if "login" in str(e).lower():
                print(f"{Fore.YELLOW}💡 Este perfil requiere autenticación. Inicia sesión desde el menú principal.{Style.RESET_ALL}")
    
    def crear_estructura_usuario(self, username: str) -> Dict[str, str]:
        """
        Crea la estructura de carpetas para un usuario específico
        
        Args:
            username: Nombre de usuario
            
        Returns:
            Dict: Rutas de las carpetas creadas
        """
        carpeta_usuario = os.path.join(self.directorio_datos, username)
        carpeta_seguidores = os.path.join(carpeta_usuario, "seguidores")
        carpeta_seguidos = os.path.join(carpeta_usuario, "seguidos")
        carpeta_reportes = os.path.join(carpeta_usuario, "reportes")
        carpeta_sesiones = os.path.join(carpeta_usuario, "sesiones")
        
        # Crear todas las carpetas
        for carpeta in [carpeta_usuario, carpeta_seguidores, carpeta_seguidos, carpeta_reportes, carpeta_sesiones]:
            if not os.path.exists(carpeta):
                os.makedirs(carpeta)
        
        return {
            "usuario": carpeta_usuario,
            "seguidores": carpeta_seguidores,
            "seguidos": carpeta_seguidos,
            "reportes": carpeta_reportes,
            "sesiones": carpeta_sesiones
        }
    
    def generar_timestamp(self) -> str:
        """
        Genera un timestamp para nombres de archivo
        
        Returns:
            str: Timestamp en formato YYYY-MM-DD_HH-MM-SS
        """
        return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    def obtener_archivo_mas_reciente(self, carpeta: str, tipo: str) -> Optional[str]:
        """
        Obtiene el archivo más reciente de un tipo específico en una carpeta
        
        Args:
            carpeta: Ruta de la carpeta
            tipo: Tipo de archivo ('seguidores', 'seguidos', 'reporte')
            
        Returns:
            Optional[str]: Ruta del archivo más reciente o None
        """
        if not os.path.exists(carpeta):
            return None
        
        archivos = [f for f in os.listdir(carpeta) if f.endswith(f'_{tipo}.json')]
        
        if not archivos:
            return None
        
        # Ordenar por fecha de modificación (más reciente primero)
        archivos_con_tiempo = []
        for archivo in archivos:
            ruta_archivo = os.path.join(carpeta, archivo)
            tiempo_mod = os.path.getmtime(ruta_archivo)
            archivos_con_tiempo.append((tiempo_mod, ruta_archivo))
        
        archivos_con_tiempo.sort(reverse=True)
        return archivos_con_tiempo[0][1]
    
    def iniciar_sesion(self, username: str, password: str) -> bool:
        """
        Inicia sesión en Instagram con manejo mejorado de errores
        
        Args:
            username: Nombre de usuario
            password: Contraseña
            
        Returns:
            bool: True si la sesión fue exitosa
        """
        try:
            print(f"{Fore.YELLOW}🔐 Iniciando sesión...{Style.RESET_ALL}")
            
            # Intentar cargar sesión existente primero
            carpetas = self.crear_estructura_usuario(username)
            archivo_sesion = os.path.join(carpetas["sesiones"], f"{username}_session")
            
            if os.path.exists(archivo_sesion):
                try:
                    print(f"{Fore.CYAN}📁 Intentando cargar sesión guardada...{Style.RESET_ALL}")
                    self.loader.load_session_from_file(username, archivo_sesion)
                    
                    # Verificar si la sesión sigue siendo válida
                    if hasattr(self.loader.context, '_session') and self.loader.context._session:
                        print(f"{Fore.GREEN}✅ Sesión guardada cargada correctamente para {username}{Style.RESET_ALL}")
                        self.sesion_activa = True
                        self.username_actual = username
                        return True
                    else:
                        print(f"{Fore.YELLOW}⚠️ La sesión guardada no es válida{Style.RESET_ALL}")
                except Exception as e:
                    print(f"{Fore.YELLOW}⚠️ Error al cargar sesión guardada: {str(e)}{Style.RESET_ALL}")
                    print(f"{Fore.CYAN}🔄 Procediendo con login manual...{Style.RESET_ALL}")
            
            # Intentar iniciar sesión manual
            try:
                self.loader.login(username, password)
                
                # Verificar que la sesión se estableció correctamente
                if hasattr(self.loader.context, '_session') and self.loader.context._session:
                    print(f"{Fore.GREEN}✅ Sesión iniciada correctamente para {username}{Style.RESET_ALL}")
                    self.sesion_activa = True
                    self.username_actual = username
                    
                    # Guardar la sesión nueva
                    try:
                        self.loader.save_session_to_file(archivo_sesion)
                        print(f"{Fore.GREEN}💾 Sesión guardada en: {archivo_sesion}{Style.RESET_ALL}")
                    except Exception as e:
                        print(f"{Fore.YELLOW}⚠️ No se pudo guardar la sesión: {str(e)}{Style.RESET_ALL}")
                    
                    return True
                else:
                    print(f"{Fore.RED}❌ No se pudo establecer la sesión correctamente{Style.RESET_ALL}")
                    return False
                    
            except instaloader.TwoFactorAuthRequiredException:
                print(f"{Fore.YELLOW}🔒 Se requiere autenticación de dos factores{Style.RESET_ALL}")
                codigo_2fa = input(f"{Fore.CYAN}Ingresa el código 2FA: {Style.RESET_ALL}")
                
                try:
                    self.loader.two_factor_login(codigo_2fa)
                    print(f"{Fore.GREEN}✅ Autenticación 2FA exitosa para {username}{Style.RESET_ALL}")
                    self.sesion_activa = True
                    self.username_actual = username
                    
                    # Guardar la sesión
                    try:
                        self.loader.save_session_to_file(archivo_sesion)
                        print(f"{Fore.GREEN}💾 Sesión guardada{Style.RESET_ALL}")
                    except Exception as e:
                        print(f"{Fore.YELLOW}⚠️ No se pudo guardar la sesión: {str(e)}{Style.RESET_ALL}")
                    
                    return True
                except Exception as e:
                    print(f"{Fore.RED}❌ Error en autenticación 2FA: {str(e)}{Style.RESET_ALL}")
                    return False
                    
            except instaloader.BadCredentialsException:
                print(f"{Fore.RED}❌ Credenciales incorrectas para {username}{Style.RESET_ALL}")
                return False
            except instaloader.exceptions.ConnectionException as e:
                print(f"{Fore.RED}❌ Error de conexión: {str(e)}{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}💡 Verifica tu conexión a internet{Style.RESET_ALL}")
                return False
            except Exception as e:
                print(f"{Fore.RED}❌ Error inesperado al iniciar sesión: {str(e)}{Style.RESET_ALL}")
                return False
                
        except Exception as e:
            print(f"{Fore.RED}❌ Error crítico en iniciar_sesion: {str(e)}{Style.RESET_ALL}")
            return False
    
    def guardar_sesion(self) -> bool:
        """
        Guarda la sesión actual en un archivo
        
        Returns:
            bool: True si se guardó correctamente
        """
        if not self.sesion_activa:
            print(f"{Fore.RED}❌ No hay sesión activa para guardar{Style.RESET_ALL}")
            return False
        
        try:
            # Crear estructura de carpetas para el usuario
            carpetas = self.crear_estructura_usuario(self.username_actual)
            archivo_sesion = os.path.join(carpetas["sesiones"], f"{self.username_actual}_session")
            self.loader.save_session_to_file(archivo_sesion)
            print(f"{Fore.GREEN}✅ Sesión guardada correctamente{Style.RESET_ALL}")
            return True
        except Exception as e:
            print(f"{Fore.RED}❌ Error al guardar sesión: {e}{Style.RESET_ALL}")
            return False
    
    def cargar_sesion(self) -> bool:
        """
        Carga una sesión desde archivo
        
        Returns:
            bool: True si se cargó correctamente
        """
        try:
            # Buscar usuarios con sesiones guardadas
            usuarios_con_sesiones = []
            
            if os.path.exists(self.directorio_datos):
                for usuario in os.listdir(self.directorio_datos):
                    carpeta_usuario = os.path.join(self.directorio_datos, usuario)
                    if os.path.isdir(carpeta_usuario):
                        carpeta_sesiones = os.path.join(carpeta_usuario, "sesiones")
                        if os.path.exists(carpeta_sesiones):
                            archivos_sesion = [f for f in os.listdir(carpeta_sesiones) if f.endswith('_session')]
                            if archivos_sesion:
                                usuarios_con_sesiones.append((usuario, os.path.join(carpeta_sesiones, archivos_sesion[0])))
            
            if not usuarios_con_sesiones:
                print(f"{Fore.RED}❌ No se encontraron sesiones guardadas{Style.RESET_ALL}")
                return False
            
            print(f"{Fore.YELLOW}Sesiones disponibles:{Style.RESET_ALL}")
            for i, (usuario, _) in enumerate(usuarios_con_sesiones, 1):
                print(f"{i}. {usuario}")
            
            seleccion = input(f"{Fore.CYAN}Selecciona una sesión (número): {Style.RESET_ALL}")
            
            try:
                indice = int(seleccion) - 1
                if 0 <= indice < len(usuarios_con_sesiones):
                    username, archivo_sesion = usuarios_con_sesiones[indice]
                    self.loader.load_session_from_file(username, archivo_sesion)
                    
                    self.username_actual = username
                    self.sesion_activa = True
                    
                    print(f"{Fore.GREEN}✅ Sesión cargada para {username}{Style.RESET_ALL}")
                    return True
                else:
                    print(f"{Fore.RED}❌ Selección inválida{Style.RESET_ALL}")
                    return False
            except ValueError:
                print(f"{Fore.RED}❌ Entrada inválida{Style.RESET_ALL}")
                return False
                
        except Exception as e:
            print(f"{Fore.RED}❌ Error al cargar sesión: {e}{Style.RESET_ALL}")
            return False
    
    def cerrar_sesion(self) -> None:
        """Cierra la sesión actual"""
        if self.sesion_activa:
            self.sesion_activa = False
            self.username_actual = None
            self.loader = instaloader.Instaloader()  # Reiniciar loader
            print(f"{Fore.GREEN}✅ Sesión cerrada correctamente{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}⚠️ No hay sesión activa{Style.RESET_ALL}")
    
    def mostrar_estado_sesion(self) -> None:
        """Muestra el estado actual de la sesión"""
        print(f"\n{Fore.YELLOW}📊 Estado del Sistema:{Style.RESET_ALL}")
        
        if self.modo_publico:
            print(f"{Fore.CYAN}🌐 Modo: Solo perfiles públicos")
            print(f"🔓 Autenticación: No requerida")
            print(f"👁️ Acceso: Solo perfiles públicos")
            print(f"🛡️ Riesgo: Muy bajo{Style.RESET_ALL}")
        elif self.sesion_activa:
            print(f"{Fore.GREEN}✅ Sesión activa")
            print(f"👤 Usuario: {self.username_actual}")
            print(f"🔐 Autenticación: Con sesión")
            print(f"👁️ Acceso: Perfiles públicos y privados{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}❌ No hay sesión activa ni modo público")
            print(f"💡 Opciones disponibles:")
            print(f"  • Iniciar sesión (acceso completo)")
            print(f"  • Activar modo público (solo perfiles públicos){Style.RESET_ALL}")
    
    def obtener_seguidores(self, username: str) -> Set[str]:
        """
        Obtiene la lista de seguidores de un usuario con validaciones mejoradas y guardado parcial
        
        Args:
            username: Nombre de usuario
            
        Returns:
            Set[str]: Conjunto de nombres de usuarios seguidores
        """
        try:
            # Validar que hay sesión activa O modo público
            if not self.sesion_activa and not self.modo_publico:
                print(f"{Fore.RED}❌ Necesitas iniciar sesión o activar modo público primero.{Style.RESET_ALL}")
                return set()
            
            # Validar y limpiar el nombre de usuario
            username = limpiar_username(username)
            if not validar_username(username):
                print(f"{Fore.RED}❌ Nombre de usuario inválido: {username}{Style.RESET_ALL}")
                return set()
            
            # En lugar de verificar acceso general, verificamos directamente al intentar obtener seguidores
            # La nueva lógica de perfiles privados se maneja más abajo
            
            print(f"{Fore.YELLOW}📥 Obteniendo seguidores de {username}...{Style.RESET_ALL}")
            if self.modo_publico:
                print(f"{Fore.CYAN}🌐 Modo público: solo perfiles públicos{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}⚠️ Advertencia: Instagram requiere autenticación para obtener listas de seguidores{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}💡 Para obtener seguidores necesitas iniciar sesión (opción 1 del menú principal){Style.RESET_ALL}")
                return set()
            
            # Verificar si hay datos parciales para continuar
            datos_parciales = self._recuperar_datos_parciales(username, 'seguidores')
            if datos_parciales:
                seguidores, timestamp = datos_parciales
                print(f"{Fore.CYAN}🔄 Continuando desde {len(seguidores)} seguidores guardados...{Style.RESET_ALL}")
            else:
                seguidores = set()
                timestamp = self.generar_timestamp()
            
            # Obtener perfil con manejo de errores específicos
            try:
                profile = instaloader.Profile.from_username(self.loader.context, username)
            except instaloader.exceptions.ProfileNotExistsException:
                print(f"{Fore.RED}❌ El perfil '{username}' no existe{Style.RESET_ALL}")
                return set()
            except instaloader.exceptions.LoginRequiredException:
                print(f"{Fore.RED}❌ Se requiere iniciar sesión para acceder a este perfil{Style.RESET_ALL}")
                return set()
            except instaloader.exceptions.PrivateProfileNotFollowedException:
                print(f"{Fore.RED}❌ El perfil '{username}' es privado y no lo sigues{Style.RESET_ALL}")
                return set()
            except Exception as e:
                print(f"{Fore.RED}❌ Error al obtener el perfil: {str(e)}{Style.RESET_ALL}")
                return set()
            
            # Verificar si el perfil es privado
            if profile.is_private:
                if self.modo_publico:
                    print(f"{Fore.RED}❌ El perfil '{username}' es privado y estás en modo público{Style.RESET_ALL}")
                    print(f"{Fore.YELLOW}💡 Cambia a modo con sesión para acceder a perfiles privados{Style.RESET_ALL}")
                    return set()
                else:
                    # Para perfiles privados, intentar acceder a los seguidores directamente
                    # Instagram permite esto si tienes acceso al perfil
                    print(f"{Fore.YELLOW}🔒 Perfil privado detectado - verificando acceso...{Style.RESET_ALL}")
                    try:
                        # Intentar obtener al menos un seguidor para verificar acceso
                        test_followers = list(profile.get_followers())
                        print(f"{Fore.GREEN}✅ Acceso confirmado al perfil privado{Style.RESET_ALL}")
                    except instaloader.exceptions.PrivateProfileNotFollowedException:
                        print(f"{Fore.RED}❌ El perfil '{username}' es privado y no tienes acceso{Style.RESET_ALL}")
                        print(f"{Fore.YELLOW}💡 Debes seguir al perfil para acceder a sus seguidores{Style.RESET_ALL}")
                        return set()
                    except Exception as e:
                        if "private" in str(e).lower() or "follow" in str(e).lower():
                            print(f"{Fore.RED}❌ No tienes acceso al perfil privado '{username}'{Style.RESET_ALL}")
                            print(f"{Fore.YELLOW}💡 Debes seguir al perfil para acceder a sus seguidores{Style.RESET_ALL}")
                            return set()
                        else:
                            print(f"{Fore.YELLOW}⚠️ Error al verificar acceso: {str(e)}{Style.RESET_ALL}")
                            print(f"{Fore.CYAN}🔄 Continuando con la obtención...{Style.RESET_ALL}")
            
            total_estimado = profile.followers
            
            print(f"  Total estimado: {formatear_numero(total_estimado)}")
            if len(seguidores) > 0:
                print(f"  Ya obtenidos: {formatear_numero(len(seguidores))}")
                print(f"  Restantes: {formatear_numero(total_estimado - len(seguidores))}")
            
            # Verificar si la cuenta tiene demasiados seguidores
            if total_estimado > 10000:
                if not confirmar_accion(f"El perfil tiene {formatear_numero(total_estimado)} seguidores. Esto puede tardar mucho tiempo. ¿Continuar?"):
                    print(f"{Fore.YELLOW}⚠️ Operación cancelada por el usuario{Style.RESET_ALL}")
                    return set()
            
            try:
                contador = len(seguidores)  # Empezar desde donde se quedó
                seguidores_ya_obtenidos = len(seguidores)
                
                for follower in profile.get_followers():
                    # Si ya tenemos este seguidor, saltarlo
                    if follower.username in seguidores:
                        continue
                        
                    seguidores.add(follower.username)
                    contador += 1
                    
                    # Guardado parcial cada 250 elementos nuevos
                    elementos_nuevos = contador - seguidores_ya_obtenidos
                    if elementos_nuevos > 0 and elementos_nuevos % 250 == 0:
                        self._guardar_datos_parciales(username, seguidores, 'seguidores', timestamp)
                    
                    # Delay inteligente cada pocos elementos
                    if elementos_nuevos % 10 == 0:
                        self._wait_if_needed()
                    
                    # Mostrar progreso cada 25 elementos o cada 1% si es más de 2500
                    intervalo = min(25, max(1, total_estimado // 100))
                    if elementos_nuevos % intervalo == 0:
                        mostrar_barra_progreso(contador, total_estimado)
                    
                    # Pausa más larga cada 100 elementos
                    if elementos_nuevos % 100 == 0:
                        print(f"\n{Fore.CYAN}  📊 Procesados {formatear_numero(contador)} seguidores - Pausa de seguridad...{Style.RESET_ALL}")
                        time.sleep(random.uniform(3.0, 7.0))
                    
                    # Si llevamos mucho tiempo, preguntar si continuar
                    if elementos_nuevos % 500 == 0 and elementos_nuevos > 0:
                        if not confirmar_accion(f"Se han procesado {contador} seguidores. ¿Continuar? (Instagram puede detectar actividad automatizada)"):
                            print(f"{Fore.YELLOW}⚠️ Operación detenida por el usuario en {contador} seguidores{Style.RESET_ALL}")
                            # Guardar progreso antes de salir
                            self._guardar_datos_parciales(username, seguidores, 'seguidores', timestamp)
                            return seguidores
                
                # Completar la barra de progreso
                mostrar_barra_progreso(len(seguidores), len(seguidores))
                print()  # Nueva línea después de la barra
                
                # Guardar archivo final y eliminar parcial
                self._finalizar_archivo_parcial(username, seguidores, 'seguidores', timestamp)
                
                print(f"{Fore.GREEN}✅ Total de seguidores obtenidos: {formatear_numero(len(seguidores))}{Style.RESET_ALL}")
                return seguidores
                
            except instaloader.exceptions.ConnectionException as e:
                error_msg = str(e)
                print(f"\n{Fore.RED}❌ Error de conexión: {error_msg}{Style.RESET_ALL}")
                
                # Guardar progreso antes de manejar el error
                if len(seguidores) > 0:
                    self._guardar_datos_parciales(username, seguidores, 'seguidores', timestamp)
                
                # Manejar rate limiting específicamente
                if self._handle_rate_limit_error(error_msg):
                    print(f"{Fore.CYAN}🔄 Reintentando obtener seguidores...{Style.RESET_ALL}")
                    return seguidores
                else:
                    print(f"{Fore.YELLOW}💡 Se obtuvieron {len(seguidores)} seguidores antes del error{Style.RESET_ALL}")
                    return seguidores
                    
            except Exception as e:
                error_msg = str(e)
                print(f"\n{Fore.RED}❌ Error durante la obtención: {error_msg}{Style.RESET_ALL}")
                
                # Guardar progreso antes de manejar el error
                if len(seguidores) > 0:
                    self._guardar_datos_parciales(username, seguidores, 'seguidores', timestamp)
                
                # Verificar si es un error de rate limiting
                if "rate limit" in error_msg.lower() or "Please wait" in error_msg:
                    if self._handle_rate_limit_error(error_msg):
                        return seguidores
                
                print(f"{Fore.YELLOW}💡 Se obtuvieron {len(seguidores)} seguidores antes del error{Style.RESET_ALL}")
                return seguidores
            
        except Exception as e:
            print(f"{Fore.RED}❌ Error crítico al obtener seguidores: {str(e)}{Style.RESET_ALL}")
            return set()
    
    def obtener_seguidos(self, username: str) -> Set[str]:
        """
        Obtiene la lista de usuarios seguidos por un usuario con validaciones mejoradas y guardado parcial
        
        Args:
            username: Nombre de usuario
            
        Returns:
            Set[str]: Conjunto de nombres de usuarios seguidos
        """
        try:
            # Validar que hay sesión activa O modo público
            if not self.sesion_activa and not self.modo_publico:
                print(f"{Fore.RED}❌ Necesitas iniciar sesión o activar modo público primero.{Style.RESET_ALL}")
                return set()
            
            # Validar y limpiar el nombre de usuario
            username = limpiar_username(username)
            if not validar_username(username):
                print(f"{Fore.RED}❌ Nombre de usuario inválido: {username}{Style.RESET_ALL}")
                return set()
            
            # En lugar de verificar acceso general, verificamos directamente al intentar obtener seguidos
            # La nueva lógica de perfiles privados se maneja más abajo
            
            print(f"{Fore.YELLOW}📤 Obteniendo seguidos de {username}...{Style.RESET_ALL}")
            if self.modo_publico:
                print(f"{Fore.CYAN}🌐 Modo público: solo perfiles públicos{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}⚠️ Advertencia: Instagram requiere autenticación para obtener listas de seguidos{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}💡 Para obtener seguidos necesitas iniciar sesión (opción 1 del menú principal){Style.RESET_ALL}")
                return set()
            
            # Verificar si hay datos parciales para continuar
            datos_parciales = self._recuperar_datos_parciales(username, 'seguidos')
            if datos_parciales:
                seguidos, timestamp = datos_parciales
                print(f"{Fore.CYAN}🔄 Continuando desde {len(seguidos)} seguidos guardados...{Style.RESET_ALL}")
            else:
                seguidos = set()
                timestamp = self.generar_timestamp()
            
            # Obtener perfil con manejo de errores específicos
            try:
                profile = instaloader.Profile.from_username(self.loader.context, username)
            except instaloader.exceptions.ProfileNotExistsException:
                print(f"{Fore.RED}❌ El perfil '{username}' no existe{Style.RESET_ALL}")
                return set()
            except instaloader.exceptions.LoginRequiredException:
                print(f"{Fore.RED}❌ Se requiere iniciar sesión para acceder a este perfil{Style.RESET_ALL}")
                return set()
            except instaloader.exceptions.PrivateProfileNotFollowedException:
                print(f"{Fore.RED}❌ El perfil '{username}' es privado y no lo sigues{Style.RESET_ALL}")
                return set()
            except Exception as e:
                print(f"{Fore.RED}❌ Error al obtener el perfil: {str(e)}{Style.RESET_ALL}")
                return set()
            
            # Verificar si el perfil es privado
            if profile.is_private:
                if self.modo_publico:
                    print(f"{Fore.RED}❌ El perfil '{username}' es privado y estás en modo público{Style.RESET_ALL}")
                    print(f"{Fore.YELLOW}💡 Cambia a modo con sesión para acceder a perfiles privados{Style.RESET_ALL}")
                    return set()
                else:
                    # Para perfiles privados, intentar acceder a los seguidos directamente
                    # Instagram permite esto si tienes acceso al perfil
                    print(f"{Fore.YELLOW}🔒 Perfil privado detectado - verificando acceso...{Style.RESET_ALL}")
                    try:
                        # Intentar obtener al menos un seguido para verificar acceso
                        test_followees = list(profile.get_followees())
                        print(f"{Fore.GREEN}✅ Acceso confirmado al perfil privado{Style.RESET_ALL}")
                    except instaloader.exceptions.PrivateProfileNotFollowedException:
                        print(f"{Fore.RED}❌ El perfil '{username}' es privado y no tienes acceso{Style.RESET_ALL}")
                        print(f"{Fore.YELLOW}💡 Debes seguir al perfil para acceder a sus seguidos{Style.RESET_ALL}")
                        return set()
                    except Exception as e:
                        if "private" in str(e).lower() or "follow" in str(e).lower():
                            print(f"{Fore.RED}❌ No tienes acceso al perfil privado '{username}'{Style.RESET_ALL}")
                            print(f"{Fore.YELLOW}💡 Debes seguir al perfil para acceder a sus seguidos{Style.RESET_ALL}")
                            return set()
                        else:
                            print(f"{Fore.YELLOW}⚠️ Error al verificar acceso: {str(e)}{Style.RESET_ALL}")
                            print(f"{Fore.CYAN}🔄 Continuando con la obtención...{Style.RESET_ALL}")
            
            total_estimado = profile.followees
            
            print(f"  Total estimado: {formatear_numero(total_estimado)}")
            if len(seguidos) > 0:
                print(f"  Ya obtenidos: {formatear_numero(len(seguidos))}")
                print(f"  Restantes: {formatear_numero(total_estimado - len(seguidos))}")
            
            # Verificar si la cuenta sigue a demasiados usuarios
            if total_estimado > 7500:
                if not confirmar_accion(f"El perfil sigue a {formatear_numero(total_estimado)} usuarios. Esto puede tardar mucho tiempo. ¿Continuar?"):
                    print(f"{Fore.YELLOW}⚠️ Operación cancelada por el usuario{Style.RESET_ALL}")
                    return set()
            
            try:
                contador = len(seguidos)  # Empezar desde donde se quedó
                seguidos_ya_obtenidos = len(seguidos)
                
                for followee in profile.get_followees():
                    # Si ya tenemos este seguido, saltarlo
                    if followee.username in seguidos:
                        continue
                        
                    seguidos.add(followee.username)
                    contador += 1
                    
                    # Guardado parcial cada 250 elementos nuevos
                    elementos_nuevos = contador - seguidos_ya_obtenidos
                    if elementos_nuevos > 0 and elementos_nuevos % 250 == 0:
                        self._guardar_datos_parciales(username, seguidos, 'seguidos', timestamp)
                    
                    # Delay inteligente cada pocos elementos
                    if elementos_nuevos % 10 == 0:
                        self._wait_if_needed()
                    
                    # Mostrar progreso cada 25 elementos o cada 1% si es más de 2500
                    intervalo = min(25, max(1, total_estimado // 100))
                    if elementos_nuevos % intervalo == 0:
                        mostrar_barra_progreso(contador, total_estimado)
                    
                    # Pausa más larga cada 100 elementos
                    if elementos_nuevos % 100 == 0:
                        print(f"\n{Fore.CYAN}  📊 Procesados {formatear_numero(contador)} seguidos - Pausa de seguridad...{Style.RESET_ALL}")
                        time.sleep(random.uniform(3.0, 7.0))
                    
                    # Si llevamos mucho tiempo, preguntar si continuar
                    if elementos_nuevos % 500 == 0 and elementos_nuevos > 0:
                        if not confirmar_accion(f"Se han procesado {contador} seguidos. ¿Continuar? (Instagram puede detectar actividad automatizada)"):
                            print(f"{Fore.YELLOW}⚠️ Operación detenida por el usuario en {contador} seguidos{Style.RESET_ALL}")
                            # Guardar progreso antes de salir
                            self._guardar_datos_parciales(username, seguidos, 'seguidos', timestamp)
                            return seguidos
                
                # Completar la barra de progreso
                mostrar_barra_progreso(len(seguidos), len(seguidos))
                print()  # Nueva línea después de la barra
                
                # Guardar archivo final y eliminar parcial
                self._finalizar_archivo_parcial(username, seguidos, 'seguidos', timestamp)
                
                print(f"{Fore.GREEN}✅ Total de seguidos obtenidos: {formatear_numero(len(seguidos))}{Style.RESET_ALL}")
                return seguidos
                
            except instaloader.exceptions.ConnectionException as e:
                error_msg = str(e)
                print(f"\n{Fore.RED}❌ Error de conexión: {error_msg}{Style.RESET_ALL}")
                
                # Guardar progreso antes de manejar el error
                if len(seguidos) > 0:
                    self._guardar_datos_parciales(username, seguidos, 'seguidos', timestamp)
                
                # Manejar rate limiting específicamente
                if self._handle_rate_limit_error(error_msg):
                    print(f"{Fore.CYAN}🔄 Reintentando obtener seguidos...{Style.RESET_ALL}")
                    return seguidos
                else:
                    print(f"{Fore.YELLOW}💡 Se obtuvieron {len(seguidos)} seguidos antes del error{Style.RESET_ALL}")
                    return seguidos
                    
            except Exception as e:
                error_msg = str(e)
                print(f"\n{Fore.RED}❌ Error durante la obtención: {error_msg}{Style.RESET_ALL}")
                
                # Guardar progreso antes de manejar el error
                if len(seguidos) > 0:
                    self._guardar_datos_parciales(username, seguidos, 'seguidos', timestamp)
                
                # Verificar si es un error de rate limiting
                if "rate limit" in error_msg.lower() or "Please wait" in error_msg:
                    if self._handle_rate_limit_error(error_msg):
                        return seguidos
                
                print(f"{Fore.YELLOW}💡 Se obtuvieron {len(seguidos)} seguidos antes del error{Style.RESET_ALL}")
                return seguidos
            
        except Exception as e:
            print(f"{Fore.RED}❌ Error crítico al obtener seguidos: {str(e)}{Style.RESET_ALL}")
            return set()
            
        except Exception as e:
            print(f"{Fore.RED}❌ Error al obtener seguidos: {e}{Style.RESET_ALL}")
            return set()
    
    def cargar_datos_anteriores(self, username: str) -> Dict:
        """
        Carga los datos anteriores de monitoreo (seguidores y seguidos más recientes)
        
        Args:
            username: Nombre de usuario
            
        Returns:
            Dict: Datos anteriores o diccionario vacío
        """
        try:
            carpetas = self.crear_estructura_usuario(username)
            
            # Obtener archivos más recientes
            archivo_seguidores = self.obtener_archivo_mas_reciente(carpetas["seguidores"], "seguidores")
            archivo_seguidos = self.obtener_archivo_mas_reciente(carpetas["seguidos"], "seguidos")
            
            datos = {}
            
            # Cargar seguidores más recientes
            if archivo_seguidores:
                with open(archivo_seguidores, 'r', encoding='utf-8') as f:
                    datos_seguidores = json.load(f)
                    datos.update(datos_seguidores)
            
            # Cargar seguidos más recientes
            if archivo_seguidos:
                with open(archivo_seguidos, 'r', encoding='utf-8') as f:
                    datos_seguidos = json.load(f)
                    # Combinar datos, manteniendo la estructura
                    if datos:
                        datos["seguidos"] = datos_seguidos.get("seguidos", [])
                        datos["total_seguidos"] = datos_seguidos.get("total_seguidos", 0)
                    else:
                        datos.update(datos_seguidos)
            
            return datos
            
        except Exception as e:
            print(f"{Fore.RED}❌ Error al cargar datos anteriores: {e}{Style.RESET_ALL}")
            return {}
    
    def guardar_datos_actuales(self, username: str, seguidores: Set[str], seguidos: Set[str]) -> None:
        """
        Guarda los datos actuales de monitoreo en archivos separados con timestamp
        
        Args:
            username: Nombre de usuario
            seguidores: Conjunto de seguidores
            seguidos: Conjunto de seguidos
        """
        try:
            carpetas = self.crear_estructura_usuario(username)
            timestamp = self.generar_timestamp()
            fecha_actual = datetime.now().isoformat()
            
            # Guardar seguidores
            datos_seguidores = {
                "username": username,
                "fecha_actualizacion": fecha_actual,
                "timestamp": timestamp,
                "seguidores": list(seguidores),
                "total_seguidores": len(seguidores),
                "tipo": "seguidores"
            }
            
            archivo_seguidores = os.path.join(carpetas["seguidores"], f"{timestamp}_seguidores.json")
            with open(archivo_seguidores, 'w', encoding='utf-8') as f:
                json.dump(datos_seguidores, f, ensure_ascii=False, indent=2)
            
            # Guardar seguidos
            datos_seguidos = {
                "username": username,
                "fecha_actualizacion": fecha_actual,
                "timestamp": timestamp,
                "seguidos": list(seguidos),
                "total_seguidos": len(seguidos),
                "tipo": "seguidos"
            }
            
            archivo_seguidos = os.path.join(carpetas["seguidos"], f"{timestamp}_seguidos.json")
            with open(archivo_seguidos, 'w', encoding='utf-8') as f:
                json.dump(datos_seguidos, f, ensure_ascii=False, indent=2)
            
            print(f"{Fore.GREEN}✅ Datos guardados correctamente en:")
            print(f"   📁 Seguidores: {archivo_seguidores}")
            print(f"   📁 Seguidos: {archivo_seguidos}{Style.RESET_ALL}")
            
        except Exception as e:
            print(f"{Fore.RED}❌ Error al guardar datos: {e}{Style.RESET_ALL}")
    
    def generar_reporte_cambios(self, username: str, datos_anteriores: Dict, 
                              seguidores_actuales: Set[str], seguidos_actuales: Set[str]) -> Dict:
        """
        Genera un reporte de cambios comparando datos anteriores con actuales
        
        Args:
            username: Nombre de usuario
            datos_anteriores: Datos del monitoreo anterior
            seguidores_actuales: Seguidores actuales
            seguidos_actuales: Seguidos actuales
            
        Returns:
            Dict: Reporte de cambios
        """
        if not datos_anteriores:
            return {
                "es_primer_monitoreo": True,
                "mensaje": "Primer monitoreo realizado. Los datos han sido guardados para futuras comparaciones."
            }
        
        seguidores_anteriores = set(datos_anteriores.get("seguidores", []))
        seguidos_anteriores = set(datos_anteriores.get("seguidos", []))
        
        # Calcular cambios
        nuevos_seguidores = seguidores_actuales - seguidores_anteriores
        seguidores_perdidos = seguidores_anteriores - seguidores_actuales
        nuevos_seguidos = seguidos_actuales - seguidos_anteriores
        seguidos_eliminados = seguidos_anteriores - seguidos_actuales
        
        reporte = {
            "es_primer_monitoreo": False,
            "username": username,
            "fecha_anterior": datos_anteriores.get("fecha_actualizacion", "Desconocida"),
            "fecha_actual": datetime.now().isoformat(),
            "timestamp": self.generar_timestamp(),
            "cambios_seguidores": {
                "nuevos": list(nuevos_seguidores),
                "perdidos": list(seguidores_perdidos),
                "total_nuevos": len(nuevos_seguidores),
                "total_perdidos": len(seguidores_perdidos)
            },
            "cambios_seguidos": {
                "nuevos": list(nuevos_seguidos),
                "eliminados": list(seguidos_eliminados),
                "total_nuevos": len(nuevos_seguidos),
                "total_eliminados": len(seguidos_eliminados)
            },
            "estadisticas": {
                "seguidores_anteriores": len(seguidores_anteriores),
                "seguidores_actuales": len(seguidores_actuales),
                "seguidos_anteriores": len(seguidos_anteriores),
                "seguidos_actuales": len(seguidos_actuales),
                "cambio_neto_seguidores": len(seguidores_actuales) - len(seguidores_anteriores),
                "cambio_neto_seguidos": len(seguidos_actuales) - len(seguidos_anteriores)
            }
        }
        
        return reporte
    
    def mostrar_reporte(self, reporte: Dict) -> None:
        """
        Muestra el reporte de cambios en la consola
        
        Args:
            reporte: Diccionario con el reporte de cambios
        """
        if reporte.get("es_primer_monitoreo"):
            print(f"\n{Fore.BLUE}🎉 {reporte['mensaje']}{Style.RESET_ALL}")
            return
        
        print(f"\n{Fore.CYAN}{'='*60}")
        print(f"📊 REPORTE DE MONITOREO - {reporte['username'].upper()}")
        print(f"{'='*60}{Style.RESET_ALL}")
        
        # Estadísticas generales
        stats = reporte["estadisticas"]
        print(f"\n{Fore.YELLOW}📈 ESTADÍSTICAS:{Style.RESET_ALL}")
        print(f"  Seguidores: {stats['seguidores_anteriores']} → {stats['seguidores_actuales']} ({stats['cambio_neto_seguidores']:+d})")
        print(f"  Seguidos: {stats['seguidos_anteriores']} → {stats['seguidos_actuales']} ({stats['cambio_neto_seguidos']:+d})")
        
        # Cambios en seguidores
        cambios_seg = reporte["cambios_seguidores"]
        if cambios_seg["total_nuevos"] > 0 or cambios_seg["total_perdidos"] > 0:
            print(f"\n{Fore.GREEN}👥 CAMBIOS EN SEGUIDORES:{Style.RESET_ALL}")
            
            if cambios_seg["total_nuevos"] > 0:
                print(f"  {Fore.GREEN}✅ Nuevos seguidores ({cambios_seg['total_nuevos']}):{Style.RESET_ALL}")
                for seguidor in cambios_seg["nuevos"][:10]:  # Mostrar máximo 10
                    print(f"    + {seguidor}")
                if cambios_seg["total_nuevos"] > 10:
                    print(f"    ... y {cambios_seg['total_nuevos'] - 10} más")
            
            if cambios_seg["total_perdidos"] > 0:
                print(f"  {Fore.RED}❌ Seguidores perdidos ({cambios_seg['total_perdidos']}):{Style.RESET_ALL}")
                for seguidor in cambios_seg["perdidos"][:10]:  # Mostrar máximo 10
                    print(f"    - {seguidor}")
                if cambios_seg["total_perdidos"] > 10:
                    print(f"    ... y {cambios_seg['total_perdidos'] - 10} más")
        
        # Cambios en seguidos
        cambios_seg = reporte["cambios_seguidos"]
        if cambios_seg["total_nuevos"] > 0 or cambios_seg["total_eliminados"] > 0:
            print(f"\n{Fore.BLUE}👤 CAMBIOS EN SEGUIDOS:{Style.RESET_ALL}")
            
            if cambios_seg["total_nuevos"] > 0:
                print(f"  {Fore.GREEN}✅ Nuevos seguidos ({cambios_seg['total_nuevos']}):{Style.RESET_ALL}")
                for seguido in cambios_seg["nuevos"][:10]:  # Mostrar máximo 10
                    print(f"    + {seguido}")
                if cambios_seg["total_nuevos"] > 10:
                    print(f"    ... y {cambios_seg['total_nuevos'] - 10} más")
            
            if cambios_seg["total_eliminados"] > 0:
                print(f"  {Fore.RED}❌ Seguidos eliminados ({cambios_seg['total_eliminados']}):{Style.RESET_ALL}")
                for seguido in cambios_seg["eliminados"][:10]:  # Mostrar máximo 10
                    print(f"    - {seguido}")
                if cambios_seg["total_eliminados"] > 10:
                    print(f"    ... y {cambios_seg['total_eliminados'] - 10} más")
        
        if (cambios_seg["total_nuevos"] == 0 and cambios_seg["total_eliminados"] == 0 and
            reporte["cambios_seguidores"]["total_nuevos"] == 0 and 
            reporte["cambios_seguidores"]["total_perdidos"] == 0):
            print(f"\n{Fore.YELLOW}ℹ️ No se detectaron cambios desde el último monitoreo{Style.RESET_ALL}")
        
        print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    
    def guardar_reporte(self, username: str, reporte: Dict) -> None:
        """
        Guarda el reporte en el archivo de reportes con timestamp
        
        Args:
            username: Nombre de usuario
            reporte: Reporte a guardar
        """
        try:
            carpetas = self.crear_estructura_usuario(username)
            timestamp = reporte.get("timestamp", self.generar_timestamp())
            
            archivo_reporte = os.path.join(carpetas["reportes"], f"{timestamp}_reporte.json")
            
            with open(archivo_reporte, 'w', encoding='utf-8') as f:
                json.dump(reporte, f, ensure_ascii=False, indent=2)
            
            print(f"{Fore.GREEN}✅ Reporte guardado: {archivo_reporte}{Style.RESET_ALL}")
            
        except Exception as e:
            print(f"{Fore.RED}❌ Error al guardar reporte: {e}{Style.RESET_ALL}")
    
    def monitorear_perfil(self, username: str) -> None:
        """
        Función principal para monitorear un perfil
        
        Args:
            username: Nombre de usuario a monitorear
        """
        if not self.sesion_activa and not self.modo_publico:
            print(f"{Fore.RED}❌ Necesitas iniciar sesión o activar modo público primero{Style.RESET_ALL}")
            return
        
        # Validar y limpiar username
        if not validar_username(username):
            print(f"{Fore.RED}❌ Nombre de usuario inválido: {username}{Style.RESET_ALL}")
            return
        
        username = limpiar_username(username)
        print(f"\n{Fore.CYAN}🔍 Iniciando monitoreo de @{username}...{Style.RESET_ALL}")
        
        if self.modo_publico:
            print(f"{Fore.YELLOW}🌐 Modo público: solo perfiles públicos accesibles{Style.RESET_ALL}")
        
        # Cargar datos anteriores
        datos_anteriores = self.cargar_datos_anteriores(username)
        
        # Obtener datos actuales
        seguidores_actuales = self.obtener_seguidores(username)
        if not seguidores_actuales:
            return
        
        seguidos_actuales = self.obtener_seguidos(username)
        if not seguidos_actuales:
            return
        
        # Generar reporte
        reporte = self.generar_reporte_cambios(username, datos_anteriores, 
                                             seguidores_actuales, seguidos_actuales)
        
        # Mostrar reporte
        self.mostrar_reporte(reporte)
        
        # Guardar datos actuales y reporte
        self.guardar_datos_actuales(username, seguidores_actuales, seguidos_actuales)
        if not reporte.get("es_primer_monitoreo"):
            self.guardar_reporte(username, reporte)
    
    def mostrar_ultimo_reporte(self) -> None:
        """Muestra el último reporte disponible"""
        try:
            usuarios_con_reportes = []
            
            if os.path.exists(self.directorio_datos):
                for usuario in os.listdir(self.directorio_datos):
                    carpeta_usuario = os.path.join(self.directorio_datos, usuario)
                    if os.path.isdir(carpeta_usuario):
                        carpeta_reportes = os.path.join(carpeta_usuario, "reportes")
                        if os.path.exists(carpeta_reportes):
                            archivos_reportes = [f for f in os.listdir(carpeta_reportes) if f.endswith('_reporte.json')]
                            if archivos_reportes:
                                usuarios_con_reportes.append(usuario)
            
            if not usuarios_con_reportes:
                print(f"{Fore.RED}❌ No se encontraron reportes{Style.RESET_ALL}")
                return
            
            print(f"{Fore.YELLOW}Usuarios con reportes disponibles:{Style.RESET_ALL}")
            for i, usuario in enumerate(usuarios_con_reportes, 1):
                print(f"{i}. {usuario}")
            
            seleccion = input(f"{Fore.CYAN}Selecciona un usuario (número): {Style.RESET_ALL}")
            
            try:
                indice = int(seleccion) - 1
                if 0 <= indice < len(usuarios_con_reportes):
                    username = usuarios_con_reportes[indice]
                    carpetas = self.crear_estructura_usuario(username)
                    
                    archivo_reporte = self.obtener_archivo_mas_reciente(carpetas["reportes"], "reporte")
                    
                    if archivo_reporte:
                        with open(archivo_reporte, 'r', encoding='utf-8') as f:
                            reporte = json.load(f)
                        
                        self.mostrar_reporte(reporte)
                    else:
                        print(f"{Fore.RED}❌ No hay reportes para este usuario{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}❌ Selección inválida{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED}❌ Entrada inválida{Style.RESET_ALL}")
                
        except Exception as e:
            print(f"{Fore.RED}❌ Error al cargar reportes: {e}{Style.RESET_ALL}")
    
    def mostrar_estructura_archivos(self) -> None:
        """Muestra la estructura de archivos para todos los usuarios monitoreados"""
        try:
            if not os.path.exists(self.directorio_datos):
                print(f"{Fore.RED}❌ No hay datos de monitoreo{Style.RESET_ALL}")
                return
            
            usuarios = [d for d in os.listdir(self.directorio_datos) 
                       if os.path.isdir(os.path.join(self.directorio_datos, d))]
            
            if not usuarios:
                print(f"{Fore.RED}❌ No hay usuarios monitoreados{Style.RESET_ALL}")
                return
            
            print(f"\n{Fore.CYAN}{'='*60}")
            print("📁 ESTRUCTURA DE ARCHIVOS DE MONITOREO")
            print(f"{'='*60}{Style.RESET_ALL}")
            
            for usuario in usuarios:
                carpeta_usuario = os.path.join(self.directorio_datos, usuario)
                
                print(f"\n{Fore.YELLOW}👤 Usuario: {usuario}{Style.RESET_ALL}")
                
                # Mostrar seguidores
                carpeta_seguidores = os.path.join(carpeta_usuario, "seguidores")
                if os.path.exists(carpeta_seguidores):
                    archivos_seguidores = [f for f in os.listdir(carpeta_seguidores) if f.endswith('_seguidores.json')]
                    print(f"  📥 Seguidores ({len(archivos_seguidores)} archivos):")
                    for archivo in sorted(archivos_seguidores)[-3:]:  # Mostrar últimos 3
                        # Extraer timestamp del nombre del archivo de forma más robusta
                        partes = archivo.rsplit('_', 1)  # Separar desde el final
                        if len(partes) > 0:
                            timestamp = partes[0].replace('_seguidores', '')
                            print(f"    📄 {timestamp}")
                    if len(archivos_seguidores) > 3:
                        print(f"    ... y {len(archivos_seguidores) - 3} archivos más")
                
                # Mostrar seguidos
                carpeta_seguidos = os.path.join(carpeta_usuario, "seguidos")
                if os.path.exists(carpeta_seguidos):
                    archivos_seguidos = [f for f in os.listdir(carpeta_seguidos) if f.endswith('_seguidos.json')]
                    print(f"  📤 Seguidos ({len(archivos_seguidos)} archivos):")
                    for archivo in sorted(archivos_seguidos)[-3:]:  # Mostrar últimos 3
                        # Extraer timestamp del nombre del archivo de forma más robusta
                        partes = archivo.rsplit('_', 1)  # Separar desde el final
                        if len(partes) > 0:
                            timestamp = partes[0].replace('_seguidos', '')
                            print(f"    📄 {timestamp}")
                    if len(archivos_seguidos) > 3:
                        print(f"    ... y {len(archivos_seguidos) - 3} archivos más")
                
                # Mostrar reportes
                carpeta_reportes = os.path.join(carpeta_usuario, "reportes")
                if os.path.exists(carpeta_reportes):
                    archivos_reportes = [f for f in os.listdir(carpeta_reportes) if f.endswith('_reporte.json')]
                    print(f"  📊 Reportes ({len(archivos_reportes)} archivos):")
                    for archivo in sorted(archivos_reportes)[-3:]:  # Mostrar últimos 3
                        # Extraer timestamp del nombre del archivo de forma más robusta
                        partes = archivo.rsplit('_', 1)  # Separar desde el final
                        if len(partes) > 0:
                            timestamp = partes[0].replace('_reporte', '')
                            print(f"    📄 {timestamp}")
                    if len(archivos_reportes) > 3:
                        print(f"    ... y {len(archivos_reportes) - 3} archivos más")
                
                # Mostrar sesiones
                carpeta_sesiones = os.path.join(carpeta_usuario, "sesiones")
                if os.path.exists(carpeta_sesiones):
                    archivos_sesiones = [f for f in os.listdir(carpeta_sesiones) if f.endswith('_session')]
                    if archivos_sesiones:
                        print(f"  🔐 Sesiones: {len(archivos_sesiones)} archivo(s)")
            
            print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
            
        except Exception as e:
            print(f"{Fore.RED}❌ Error al mostrar estructura: {e}{Style.RESET_ALL}")

    def limpiar_datos_monitoreo(self) -> None:
        """Limpia todos los datos de monitoreo"""
        try:
            import shutil
            
            if os.path.exists(self.directorio_datos):
                shutil.rmtree(self.directorio_datos)
                os.makedirs(self.directorio_datos)
                print(f"{Fore.GREEN}✅ Datos de monitoreo limpiados correctamente{Style.RESET_ALL}")
            else:
                print(f"{Fore.YELLOW}⚠️ No hay datos para limpiar{Style.RESET_ALL}")
            
        except Exception as e:
            print(f"{Fore.RED}❌ Error al limpiar datos: {e}{Style.RESET_ALL}")
    
    def encontrar_seguidores_mutuos(self, username1: str, username2: str) -> None:
        """
        Encuentra seguidores mutuos entre dos perfiles
        
        Args:
            username1: Primer perfil
            username2: Segundo perfil
        """
        if not self.sesion_activa and not self.modo_publico:
            print(f"{Fore.RED}❌ Necesitas iniciar sesión o activar modo público primero{Style.RESET_ALL}")
            return
        
        print(f"\n{Fore.CYAN}🔍 Analizando seguidores mutuos entre @{username1} y @{username2}...{Style.RESET_ALL}")
        
        if self.modo_publico:
            print(f"{Fore.YELLOW}🌐 Modo público: verificando que ambos perfiles sean públicos...{Style.RESET_ALL}")
        
        # Obtener seguidores de ambos perfiles
        seguidores1 = self.obtener_seguidores(username1)
        if not seguidores1:
            return
        
        seguidores2 = self.obtener_seguidores(username2)
        if not seguidores2:
            return
        
        # Encontrar intersección
        seguidores_mutuos = seguidores1.intersection(seguidores2)
        
        print(f"\n{Fore.CYAN}{'='*60}")
        print("👥 SEGUIDORES MUTUOS")
        print(f"{'='*60}{Style.RESET_ALL}")
        print(f"@{username1}: {len(seguidores1)} seguidores")
        print(f"@{username2}: {len(seguidores2)} seguidores")
        print(f"{Fore.GREEN}👥 Seguidores mutuos: {len(seguidores_mutuos)}{Style.RESET_ALL}")
        
        if seguidores_mutuos:
            print(f"\n{Fore.YELLOW}Lista de seguidores mutuos:{Style.RESET_ALL}")
            for seguidor in sorted(seguidores_mutuos):
                print(f"  • {seguidor}")
        else:
            print(f"\n{Fore.YELLOW}ℹ️ No se encontraron seguidores mutuos{Style.RESET_ALL}")
        
        print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    
    def analizar_conexiones_seguidores(self, username: str) -> None:
        """
        Analiza las conexiones entre los seguidores y seguidos del perfil
        
        Args:
            username: Perfil a analizar
        """
        if not self.sesion_activa and not self.modo_publico:
            print(f"{Fore.RED}❌ Necesitas iniciar sesión primero{Style.RESET_ALL}")
            return
            
        if self.modo_publico:
            print(f"{Fore.YELLOW}📖 Analizando en modo público - Solo perfiles públicos disponibles{Style.RESET_ALL}")
        
        print(f"\n{Fore.CYAN}🔍 Analizando conexiones internas de @{username}...{Style.RESET_ALL}")
        
        # Obtener seguidores y seguidos
        seguidores = self.obtener_seguidores(username)
        if not seguidores:
            return
        
        seguidos = self.obtener_seguidos(username)
        if not seguidos:
            return
        
        # Encontrar intersecciones
        sigue_a_seguidores = seguidores.intersection(seguidos)  # Usuarios que son seguidores Y seguidos
        
        print(f"\n{Fore.CYAN}{'='*60}")
        print("🔗 ANÁLISIS DE CONEXIONES INTERNAS")
        print(f"{'='*60}{Style.RESET_ALL}")
        print(f"@{username}:")
        print(f"  📥 Seguidores: {len(seguidores)}")
        print(f"  📤 Seguidos: {len(seguidos)}")
        print(f"  {Fore.GREEN}🔄 Conexiones mutuas: {len(sigue_a_seguidores)}{Style.RESET_ALL}")
        
        if sigue_a_seguidores:
            print(f"\n{Fore.YELLOW}👥 Usuarios con conexión mutua (son seguidores Y seguidos):{Style.RESET_ALL}")
            for usuario in sorted(sigue_a_seguidores):
                print(f"  • {usuario}")
        
        # Calcular ratio de reciprocidad
        if len(seguidores) > 0:
            ratio_reciprocidad = (len(sigue_a_seguidores) / len(seguidores)) * 100
            print(f"\n{Fore.BLUE}📊 Ratio de reciprocidad: {ratio_reciprocidad:.1f}%{Style.RESET_ALL}")
        
        print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
