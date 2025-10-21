# Sistema de Gestión de Clientes

Un sistema de línea de comandos para gestionar información de clientes desde archivos CSV.

## Características

- Carga de datos desde archivos CSV
- Búsqueda de clientes por ID
- Listado de clientes por ciudad
- Ordenamiento de clientes por edad
- Resumen de carga de datos
- Manejo robusto de errores

## Instalación

1. Instalar las dependencias:
```bash
pip install -r requirements.txt
```

## Uso

### Menú Interactivo

Para una experiencia más fácil, puedes ejecutar el programa sin argumentos para acceder al menú interactivo:

```bash
python main.py
```

Esto mostrará un menú con las siguientes opciones:
1. Mostrar resumen de carga
2. Buscar cliente por ID
3. Listar clientes por ciudad
4. Ordenar clientes por edad
5. Cambiar archivo CSV
6. Salir

### Comandos de línea de comandos

#### Mostrar resumen de carga
```bash
python main.py summary
```

#### Buscar cliente por ID
```bash
python main.py get --id 1983
```

#### Listar clientes por ciudad
```bash
python main.py list-city --city "Quito"
```

#### Ordenar clientes por edad
```bash
python main.py sort-age
```

#### Especificar archivo CSV personalizado
```bash
python main.py --csv mi_archivo.csv summary
```

### Ejemplos

```bash
# Mostrar ayuda
python main.py --help

# Resumen de la carga de datos
python main.py summary

# Buscar un cliente específico
python main.py get --id 1983

# Listar todos los clientes de Quito
python main.py list-city --city "Quito"

# Ver clientes ordenados por edad (más jóvenes primero)
python main.py sort-age
```

## Estructura del proyecto

```
├── main.py                 # Punto de entrada principal
├── modules/
│   ├── __init__.py        # Inicialización del módulo
│   ├── csv_loader.py      # Carga y procesamiento de CSV
│   ├── customer_manager.py # Gestión de clientes
│   ├── models.py          # Modelos de datos
│   └── printer.py         # Funciones de impresión
├── tests/
│   └── test_basic.py      # Pruebas básicas
├── clientes.csv           # Archivo de datos de ejemplo
├── requirements.txt       # Dependencias del proyecto
└── README.md             # Este archivo
```

## Formato del archivo CSV

El archivo CSV debe contener las siguientes columnas:
- `id`: Identificador único del cliente (entero)
- `nombre`: Nombre del cliente (texto)
- `email`: Correo electrónico (texto)
- `ciudad`: Ciudad de residencia (texto)
- `edad`: Edad del cliente (entero)

## Manejo de errores

El sistema maneja automáticamente:
- Archivos CSV inexistentes o vacíos
- Datos inválidos en el CSV
- IDs de clientes no encontrados
- Ciudades sin clientes
- Errores de formato en los datos

## Requisitos del sistema

- Python 3.7 o superior
- pandas 1.1.5 o superior
