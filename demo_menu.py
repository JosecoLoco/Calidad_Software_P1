#!/usr/bin/env python3
"""
Script de demostración del menú interactivo
"""

import subprocess
import sys
import time

def demo_menu():
    """Demuestra el menú interactivo con entradas automáticas"""
    
    print("=" * 60)
    print("    DEMOSTRACIÓN DEL MENÚ INTERACTIVO")
    print("=" * 60)
    print()
    print("Este script demuestra las funcionalidades del menú:")
    print("1. Resumen de carga")
    print("2. Búsqueda por ID")
    print("3. Listado por ciudad")
    print("4. Ordenamiento por edad")
    print("5. Cambio de archivo CSV")
    print()
    print("Para usar el menú interactivo, ejecuta:")
    print("    python main.py")
    print()
    print("Para usar comandos directos, ejecuta:")
    print("    python main.py summary")
    print("    python main.py get --id 1983")
    print("    python main.py list-city --city 'Quito'")
    print("    python main.py sort-age")
    print()
    print("=" * 60)

if __name__ == "__main__":
    demo_menu()
