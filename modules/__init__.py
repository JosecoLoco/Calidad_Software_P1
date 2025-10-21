"""
Módulo de gestión de clientes.

Este módulo proporciona funcionalidades para cargar, gestionar y consultar
información de clientes desde archivos CSV.
"""

from .csv_loader import CsvLoader
from .customer_manager import CustomerManager
from .models import Cliente
from .printer import print_cliente, print_lista, print_resumen, print_error, print_info

__all__ = [
    'CsvLoader',
    'CustomerManager', 
    'Cliente',
    'print_cliente',
    'print_lista',
    'print_resumen',
    'print_error',
    'print_info'
]
