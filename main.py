import argparse
import sys
import os
from typing import List

from modules.csv_loader import CsvLoader
from modules.customer_manager import CustomerManager
from modules.printer import print_cliente, print_lista, print_resumen, print_error, print_info


def clear_screen():
    """Limpia la pantalla de la consola"""
    os.system('cls' if os.name == 'nt' else 'clear')


def show_menu():
    """Muestra el menú principal"""
    print("=" * 50)
    print("    SISTEMA DE GESTIÓN DE CLIENTES")
    print("=" * 50)
    print("1. Mostrar resumen de carga")
    print("2. Buscar cliente por ID")
    print("3. Listar clientes por ciudad")
    print("4. Ordenar clientes por edad")
    print("5. Cambiar archivo CSV")
    print("6. Salir")
    print("=" * 50)


def get_user_choice():
    """Obtiene la opción del usuario"""
    while True:
        try:
            choice = input("Seleccione una opción (1-6): ").strip()
            if choice in ['1', '2', '3', '4', '5', '6']:
                return choice
            else:
                print_error("Opción inválida. Por favor seleccione 1-6.")
        except (KeyboardInterrupt, EOFError):
            print("\n")
            return '6'


def handle_summary(cm, loader):
    """Maneja la opción de resumen"""
    clear_screen()
    print("RESUMEN DE CARGA")
    print("-" * 30)
    print_resumen(loader.resumen())
    input("\nPresione Enter para continuar...")


def handle_search_by_id(cm):
    """Maneja la búsqueda por ID"""
    clear_screen()
    print("BÚSQUEDA POR ID")
    print("-" * 30)
    
    while True:
        try:
            client_id = input("Ingrese el ID del cliente: ").strip()
            if not client_id:
                print_error("ID no puede estar vacío")
                continue
            
            # Validar que sea un número
            if not client_id.isdigit():
                print_error("ID debe ser un número entero válido. Intente nuevamente.")
                continue
            
            client_id = int(client_id)
            if client_id < 0:
                print_error("ID debe ser un número positivo")
                continue
                
            cliente = cm.buscar_por_id(client_id)
            if cliente:
                print_cliente(cliente)
            else:
                print_info("Cliente no encontrado")
            
            input("\nPresione Enter para continuar...")
            break
            
        except ValueError:
            print_error("ID debe ser un número entero válido")
        except (KeyboardInterrupt, EOFError):
            break


def handle_list_by_city(cm):
    """Maneja el listado por ciudad"""
    clear_screen()
    print("LISTADO POR CIUDAD")
    print("-" * 30)
    
    while True:
        try:
            city = input("Ingrese el nombre de la ciudad: ").strip()
            if not city:
                print_error("Ciudad no puede estar vacía")
                continue
            
            # Validar que no sea solo números
            if city.isdigit():
                print_error("La ciudad debe ser un nombre, no un número. Intente nuevamente.")
                continue
            
            # Validar que no sea solo caracteres especiales o números
            if not any(c.isalpha() for c in city):
                print_error("La ciudad debe contener al menos algunas letras. Intente nuevamente.")
                continue
            
            clientes = cm.listar_por_ciudad(city)
            if clientes:
                print(f"\nClientes encontrados en {city}:")
                print_lista(clientes)
            else:
                print_info(f"Sin clientes para la ciudad '{city}'")
            
            input("\nPresione Enter para continuar...")
            break
            
        except (KeyboardInterrupt, EOFError):
            break


def handle_sort_by_age(cm):
    """Maneja el ordenamiento por edad"""
    clear_screen()
    print("CLIENTES ORDENADOS POR EDAD")
    print("-" * 30)
    
    clientes = cm.ordenar_por_edad()
    if clientes:
        print(f"Total de clientes: {len(clientes)}")
        print_lista(clientes)
    else:
        print_info("No hay clientes para mostrar")
    
    input("\nPresione Enter para continuar...")


def handle_change_csv():
    """Maneja el cambio de archivo CSV"""
    clear_screen()
    print("CAMBIAR ARCHIVO CSV")
    print("-" * 30)
    
    while True:
        try:
            csv_file = input("Ingrese la ruta del archivo CSV: ").strip()
            if not csv_file:
                print_error("Ruta no puede estar vacía")
                continue
            
            if not os.path.exists(csv_file):
                print_error(f"Archivo '{csv_file}' no encontrado")
                continue
            
            return csv_file
            
        except (KeyboardInterrupt, EOFError):
            return None


def interactive_menu():
    """Menú interactivo principal"""
    csv_file = "clientes.csv"
    cm = None
    loader = None
    
    while True:
        try:
            # Cargar datos si es necesario
            if cm is None:
                try:
                    loader = CsvLoader(csv_file)
                    clientes = loader.cargar()
                    cm = CustomerManager(clientes)
                    print_info(f"Datos cargados desde: {csv_file}")
                except Exception as e:
                    print_error(f"Error al cargar datos: {e}")
                    csv_file = "clientes.csv"
                    continue
            
            clear_screen()
            show_menu()
            choice = get_user_choice()
            
            if choice == '1':
                handle_summary(cm, loader)
            elif choice == '2':
                handle_search_by_id(cm)
            elif choice == '3':
                handle_list_by_city(cm)
            elif choice == '4':
                handle_sort_by_age(cm)
            elif choice == '5':
                new_csv = handle_change_csv()
                if new_csv:
                    csv_file = new_csv
                    cm = None  # Forzar recarga
                    loader = None
            elif choice == '6':
                print_info("¡Hasta luego!")
                break
                
        except (KeyboardInterrupt, EOFError):
            print("\n")
            print_info("¡Hasta luego!")
            break
        except Exception as e:
            print_error(f"Error inesperado: {e}")
            input("Presione Enter para continuar...")


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="clientes-cli", description="Gestión de clientes (consola)")
    p.add_argument("--csv", default="clientes.csv", help="Ruta del archivo CSV (por defecto: clientes.csv)")
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("summary", help="Mostrar resumen de la última carga")

    g = sub.add_parser("get", help="Buscar cliente por ID")
    g.add_argument("--id", type=int, required=True)

    lc = sub.add_parser("list-city", help="Listar clientes por ciudad")
    lc.add_argument("--city", required=True)

    sub.add_parser("sort-age", help="Listar clientes ordenados por edad (ascendente)")
    return p


def main(argv: List[str]) -> int:
    # Si no hay argumentos, mostrar menú interactivo
    if not argv:
        try:
            interactive_menu()
            return 0
        except Exception as e:
            print_error(f"Error en el menú interactivo: {e}")
            return 1
    
    # Modo línea de comandos tradicional
    parser = build_parser()
    args = parser.parse_args(argv)

    # Carga inicial obligatoria (RF1): si falla, error claro y salida controlada
    try:
        loader = CsvLoader(args.csv)
        clientes = loader.cargar()
        cm = CustomerManager(clientes)
    except FileNotFoundError as e:
        print_error(str(e))
        return 2
    except Exception as e:
        print_error(f"Error interno al cargar CSV: {e}")
        return 2

    if args.cmd == "summary":
        print_resumen(loader.resumen())
        return 0

    if args.cmd == "get":
        cid = args.id
        if cid is None or cid < 0:
            print_error("ID inválido")
            return 1
        c = cm.buscar_por_id(cid)
        if c:
            print_cliente(c)
        else:
            print_info("Cliente no encontrado")
        return 0

    if args.cmd == "list-city":
        city = args.city or ""
        res = cm.listar_por_ciudad(city)
        if not city.strip():
            print_error("Ciudad requerida")
            return 1
        if res:
            print_lista(res)
        else:
            print_info("Sin clientes para la ciudad especificada")
        return 0

    if args.cmd == "sort-age":
        res = cm.ordenar_por_edad()
        print_lista(res)
        return 0

    print_error("Comando no reconocido")
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
