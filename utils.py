#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Utilidades adicionales para el Monitor de Instagram
Funciones de ayuda y utilidades varias
"""

import os
import json
from datetime import datetime
from typing import List, Dict, Any
from colorama import Fore, Style

def formatear_fecha(fecha_iso: str) -> str:
    """
    Formatea una fecha ISO a formato legible
    
    Args:
        fecha_iso: Fecha en formato ISO
        
    Returns:
        str: Fecha formateada
    """
    try:
        fecha = datetime.fromisoformat(fecha_iso.replace('Z', '+00:00'))
        return fecha.strftime("%d/%m/%Y %H:%M:%S")
    except:
        return fecha_iso

def validar_username(username: str) -> bool:
    """
    Valida que un nombre de usuario tenga formato válido
    
    Args:
        username: Nombre de usuario a validar
        
    Returns:
        bool: True si es válido
    """
    if not username:
        return False
    
    # Eliminar @ si está presente
    username = username.lstrip('@')
    
    # Verificar longitud
    if len(username) < 1 or len(username) > 30:
        return False
    
    # Verificar caracteres válidos
    return username.replace('_', '').replace('.', '').isalnum()

def limpiar_username(username: str) -> str:
    """
    Limpia y normaliza un nombre de usuario
    
    Args:
        username: Nombre de usuario a limpiar
        
    Returns:
        str: Username limpio
    """
    return username.strip().lstrip('@').lower()

def crear_directorio_si_no_existe(directorio: str) -> bool:
    """
    Crea un directorio si no existe
    
    Args:
        directorio: Ruta del directorio
        
    Returns:
        bool: True si se creó o ya existía
    """
    try:
        if not os.path.exists(directorio):
            os.makedirs(directorio)
        return True
    except Exception as e:
        print(f"{Fore.RED}❌ Error al crear directorio {directorio}: {e}{Style.RESET_ALL}")
        return False

def listar_archivos_usuario(directorio: str, username: str) -> Dict[str, str]:
    """
    Lista todos los archivos relacionados con un usuario
    
    Args:
        directorio: Directorio de datos
        username: Nombre de usuario
        
    Returns:
        Dict: Diccionario con los archivos encontrados
    """
    archivos = {}
    
    if not os.path.exists(directorio):
        return archivos
    
    # Buscar archivos del usuario
    prefijo = f"{username}_"
    
    for archivo in os.listdir(directorio):
        if archivo.startswith(prefijo):
            ruta_completa = os.path.join(directorio, archivo)
            if archivo.endswith('_datos.json'):
                archivos['datos'] = ruta_completa
            elif archivo.endswith('_reportes.json'):
                archivos['reportes'] = ruta_completa
            elif archivo.endswith('_session'):
                archivos['sesion'] = ruta_completa
    
    return archivos

def obtener_estadisticas_archivo(archivo: str) -> Dict[str, Any]:
    """
    Obtiene estadísticas de un archivo
    
    Args:
        archivo: Ruta del archivo
        
    Returns:
        Dict: Estadísticas del archivo
    """
    stats = {
        'existe': False,
        'tamaño': 0,
        'modificado': None,
        'legible': False
    }
    
    try:
        if os.path.exists(archivo):
            stats['existe'] = True
            stat_info = os.stat(archivo)
            stats['tamaño'] = stat_info.st_size
            stats['modificado'] = datetime.fromtimestamp(stat_info.st_mtime)
            stats['legible'] = os.access(archivo, os.R_OK)
    except Exception:
        pass
    
    return stats

def mostrar_barra_progreso(actual: int, total: int, ancho: int = 50) -> None:
    """
    Muestra una barra de progreso en la consola
    
    Args:
        actual: Valor actual
        total: Valor total
        ancho: Ancho de la barra
    """
    if total == 0:
        porcentaje = 100
    else:
        porcentaje = min(100, (actual / total) * 100)
    
    lleno = int(ancho * porcentaje / 100)
    vacio = ancho - lleno
    
    barra = f"{Fore.GREEN}{'█' * lleno}{Fore.WHITE}{'░' * vacio}{Style.RESET_ALL}"
    print(f"\r  Progreso: [{barra}] {porcentaje:.1f}% ({actual}/{total})", end='', flush=True)

def calcular_diferencia_tiempo(fecha1: str, fecha2: str) -> str:
    """
    Calcula la diferencia entre dos fechas
    
    Args:
        fecha1: Fecha más antigua (ISO)
        fecha2: Fecha más reciente (ISO)
        
    Returns:
        str: Diferencia en formato legible
    """
    try:
        dt1 = datetime.fromisoformat(fecha1.replace('Z', '+00:00'))
        dt2 = datetime.fromisoformat(fecha2.replace('Z', '+00:00'))
        diferencia = dt2 - dt1
        
        dias = diferencia.days
        horas, resto = divmod(diferencia.seconds, 3600)
        minutos, _ = divmod(resto, 60)
        
        if dias > 0:
            return f"{dias} días, {horas} horas"
        elif horas > 0:
            return f"{horas} horas, {minutos} minutos"
        else:
            return f"{minutos} minutos"
    except:
        return "Tiempo desconocido"

def generar_resumen_cambios(cambios_seguidores: Dict, cambios_seguidos: Dict) -> str:
    """
    Genera un resumen corto de los cambios
    
    Args:
        cambios_seguidores: Cambios en seguidores
        cambios_seguidos: Cambios en seguidos
        
    Returns:
        str: Resumen de cambios
    """
    resumen_partes = []
    
    if cambios_seguidores['total_nuevos'] > 0:
        resumen_partes.append(f"+{cambios_seguidores['total_nuevos']} seguidores")
    
    if cambios_seguidores['total_perdidos'] > 0:
        resumen_partes.append(f"-{cambios_seguidores['total_perdidos']} seguidores")
    
    if cambios_seguidos['total_nuevos'] > 0:
        resumen_partes.append(f"+{cambios_seguidos['total_nuevos']} seguidos")
    
    if cambios_seguidos['total_eliminados'] > 0:
        resumen_partes.append(f"-{cambios_seguidos['total_eliminados']} seguidos")
    
    if not resumen_partes:
        return "Sin cambios"
    
    return ", ".join(resumen_partes)

def confirmar_accion(mensaje: str, default: bool = False) -> bool:
    """
    Pide confirmación al usuario para una acción
    
    Args:
        mensaje: Mensaje a mostrar
        default: Valor por defecto
        
    Returns:
        bool: True si el usuario confirma
    """
    opciones = "[s/N]" if not default else "[S/n]"
    respuesta = input(f"{Fore.YELLOW}{mensaje} {opciones}: {Style.RESET_ALL}").strip().lower()
    
    if not respuesta:
        return default
    
    return respuesta in ['s', 'si', 'sí', 'y', 'yes']

def formatear_numero(numero: int) -> str:
    """
    Formatea un número con separadores de miles
    
    Args:
        numero: Número a formatear
        
    Returns:
        str: Número formateado
    """
    return f"{numero:,}".replace(',', '.')

def truncar_lista(lista: List[str], max_elementos: int = 10) -> tuple:
    """
    Trunca una lista y devuelve la parte visible y el resto
    
    Args:
        lista: Lista a truncar
        max_elementos: Máximo de elementos a mostrar
        
    Returns:
        tuple: (elementos_visibles, elementos_restantes)
    """
    if len(lista) <= max_elementos:
        return lista, 0
    
    return lista[:max_elementos], len(lista) - max_elementos

def obtener_emoji_cambio(cambio: int) -> str:
    """
    Obtiene el emoji apropiado para un cambio numérico
    
    Args:
        cambio: Valor del cambio
        
    Returns:
        str: Emoji correspondiente
    """
    if cambio > 0:
        return "📈"
    elif cambio < 0:
        return "📉"
    else:
        return "➖"

def validar_rango_numero(numero: str, min_val: int = 1, max_val: int = 100) -> tuple:
    """
    Valida que un número esté en un rango específico
    
    Args:
        numero: Número como string
        min_val: Valor mínimo
        max_val: Valor máximo
        
    Returns:
        tuple: (es_valido, numero_convertido)
    """
    try:
        num = int(numero)
        if min_val <= num <= max_val:
            return True, num
        else:
            return False, None
    except ValueError:
        return False, None
