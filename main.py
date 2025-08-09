#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Programa de Monitoreo de Instagram con Consola
Desarrollado para monitorear perfiles de Instagram de forma avanzada
"""

import os
import sys
import getpass
from colorama import init, Fore, Style
from instagram_monitor import InstagramMonitor
from utils import confirmar_accion

# Inicializar colorama para colores en Windows
init()

def verificar_dependencias():
    """
    Verifica que todas las dependencias estén instaladas
    """
    dependencias_requeridas = {
        'instaloader': 'instaloader',
        'colorama': 'colorama'
    }
    
    dependencias_faltantes = []
    
    for nombre, modulo in dependencias_requeridas.items():
        try:
            __import__(modulo)
        except ImportError:
            dependencias_faltantes.append(nombre)
    
    if dependencias_faltantes:
        print(f"{Fore.RED}❌ Faltan las siguientes dependencias:{Style.RESET_ALL}")
        for dep in dependencias_faltantes:
            print(f"  - {dep}")
        print(f"\n{Fore.YELLOW}💡 Instálalas con: pip install {' '.join(dependencias_faltantes)}{Style.RESET_ALL}")
        return False
    
    return True

def mostrar_logo():
    """Muestra el logo del programa"""
    print(f"{Fore.CYAN}{Style.BRIGHT}")
    print("=" * 60)
    print("    📸 MONITOR DE INSTAGRAM - SEEYOUINSTAGRAM 📸")
    print("=" * 60)
    print(f"{Style.RESET_ALL}")

def mostrar_menu_principal():
    """Muestra el menú principal del programa"""
    print(f"\n{Fore.YELLOW}{Style.BRIGHT}MENÚ PRINCIPAL:{Style.RESET_ALL}")
    print(f"{Fore.WHITE}1. {Fore.GREEN}Gestión de Sesiones")
    print(f"{Fore.WHITE}2. {Fore.BLUE}Monitoreo de Perfil")
    print(f"{Fore.WHITE}3. {Fore.MAGENTA}Análisis de Conexiones")
    print(f"{Fore.WHITE}4. {Fore.CYAN}Ver Estado de la Sesión")
    print(f"{Fore.WHITE}5. {Fore.RED}Salir{Style.RESET_ALL}")
    print("-" * 40)

def mostrar_menu_sesiones():
    """Muestra el menú de gestión de sesiones"""
    print(f"\n{Fore.YELLOW}{Style.BRIGHT}GESTIÓN DE SESIONES:{Style.RESET_ALL}")
    print(f"{Fore.WHITE}1. {Fore.GREEN}Iniciar Sesión")
    print(f"{Fore.WHITE}2. {Fore.BLUE}Cargar Sesión Guardada")
    print(f"{Fore.WHITE}3. {Fore.MAGENTA}Guardar Sesión Actual")
    print(f"{Fore.WHITE}4. {Fore.YELLOW}Cerrar Sesión")
    print(f"{Fore.WHITE}5. {Fore.RED}Volver al Menú Principal{Style.RESET_ALL}")
    print("-" * 40)

def mostrar_menu_monitoreo():
    """Muestra el menú de monitoreo"""
    print(f"\n{Fore.YELLOW}{Style.BRIGHT}MONITOREO DE PERFIL:{Style.RESET_ALL}")
    print(f"{Fore.WHITE}1. {Fore.GREEN}Iniciar Monitoreo de Perfil")
    print(f"{Fore.WHITE}2. {Fore.BLUE}Ver Último Reporte")
    print(f"{Fore.WHITE}3. {Fore.MAGENTA}Ver Estructura de Archivos")
    print(f"{Fore.WHITE}4. {Fore.CYAN}Limpiar Datos de Monitoreo")
    print(f"{Fore.WHITE}5. {Fore.RED}Volver al Menú Principal{Style.RESET_ALL}")
    print("-" * 40)

def mostrar_menu_conexiones():
    """Muestra el menú de análisis de conexiones"""
    print(f"\n{Fore.YELLOW}{Style.BRIGHT}ANÁLISIS DE CONEXIONES:{Style.RESET_ALL}")
    print(f"{Fore.WHITE}1. {Fore.GREEN}Encontrar Seguidores Mutuos")
    print(f"{Fore.WHITE}2. {Fore.BLUE}Analizar Conexiones entre Seguidores")
    print(f"{Fore.WHITE}3. {Fore.RED}Volver al Menú Principal{Style.RESET_ALL}")
    print("-" * 40)

def manejar_sesiones(monitor):
    """Maneja el menú de sesiones"""
    while True:
        mostrar_menu_sesiones()
        opcion = input(f"{Fore.CYAN}Selecciona una opción: {Style.RESET_ALL}")
        
        if opcion == "1":
            username = input(f"{Fore.CYAN}Nombre de usuario: {Style.RESET_ALL}")
            password = getpass.getpass(f"{Fore.CYAN}Contraseña: {Style.RESET_ALL}")
            monitor.iniciar_sesion(username, password)
            
        elif opcion == "2":
            monitor.cargar_sesion()
            
        elif opcion == "3":
            monitor.guardar_sesion()
            
        elif opcion == "4":
            monitor.cerrar_sesion()
            
        elif opcion == "5":
            break
            
        else:
            print(f"{Fore.RED}Opción no válida. Intenta de nuevo.{Style.RESET_ALL}")

def manejar_monitoreo(monitor):
    """Maneja el menú de monitoreo"""
    while True:
        mostrar_menu_monitoreo()
        opcion = input(f"{Fore.CYAN}Selecciona una opción: {Style.RESET_ALL}")
        
        if opcion == "1":
            username = input(f"{Fore.CYAN}Nombre de usuario a monitorear: {Style.RESET_ALL}")
            monitor.monitorear_perfil(username)
            
        elif opcion == "2":
            monitor.mostrar_ultimo_reporte()
            
        elif opcion == "3":
            monitor.mostrar_estructura_archivos()
            
        elif opcion == "4":
            if confirmar_accion("¿Estás seguro de que quieres limpiar todos los datos?"):
                monitor.limpiar_datos_monitoreo()
                
        elif opcion == "5":
            break
            
        else:
            print(f"{Fore.RED}Opción no válida. Intenta de nuevo.{Style.RESET_ALL}")

def manejar_conexiones(monitor):
    """Maneja el menú de análisis de conexiones"""
    while True:
        mostrar_menu_conexiones()
        opcion = input(f"{Fore.CYAN}Selecciona una opción: {Style.RESET_ALL}")
        
        if opcion == "1":
            username1 = input(f"{Fore.CYAN}Primer perfil: {Style.RESET_ALL}")
            username2 = input(f"{Fore.CYAN}Segundo perfil: {Style.RESET_ALL}")
            monitor.encontrar_seguidores_mutuos(username1, username2)
            
        elif opcion == "2":
            username = input(f"{Fore.CYAN}Perfil a analizar: {Style.RESET_ALL}")
            monitor.analizar_conexiones_seguidores(username)
            
        elif opcion == "3":
            break
            
        else:
            print(f"{Fore.RED}Opción no válida. Intenta de nuevo.{Style.RESET_ALL}")

def main():
    """Función principal del programa"""
    mostrar_logo()
    
    # Crear instancia del monitor
    monitor = InstagramMonitor()
    
    while True:
        mostrar_menu_principal()
        opcion = input(f"{Fore.CYAN}Selecciona una opción: {Style.RESET_ALL}")
        
        if opcion == "1":
            manejar_sesiones(monitor)
            
        elif opcion == "2":
            if not monitor.sesion_activa:
                print(f"{Fore.RED}❌ Necesitas iniciar sesión primero.{Style.RESET_ALL}")
                continue
            manejar_monitoreo(monitor)
            
        elif opcion == "3":
            if not monitor.sesion_activa:
                print(f"{Fore.RED}❌ Necesitas iniciar sesión primero.{Style.RESET_ALL}")
                continue
            manejar_conexiones(monitor)
            
        elif opcion == "4":
            monitor.mostrar_estado_sesion()
            
        elif opcion == "5":
            print(f"{Fore.GREEN}¡Gracias por usar SeeYouInstagram! 👋{Style.RESET_ALL}")
            break
            
        else:
            print(f"{Fore.RED}Opción no válida. Intenta de nuevo.{Style.RESET_ALL}")

if __name__ == "__main__":
    try:
        # Verificar dependencias antes de empezar
        if not verificar_dependencias():
            print(f"{Fore.RED}❌ No se pueden ejecutar el programa sin las dependencias requeridas{Style.RESET_ALL}")
            sys.exit(1)
        
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Programa interrumpido por el usuario.{Style.RESET_ALL}")
        sys.exit(0)
    except Exception as e:
        print(f"{Fore.RED}Error inesperado: {e}{Style.RESET_ALL}")
        sys.exit(1)
