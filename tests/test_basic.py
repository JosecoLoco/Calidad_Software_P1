import pytest
import sys
import os

# Agregar el directorio raíz al path para importar módulos
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.models import Cliente
from modules.customer_manager import CustomerManager
from modules.csv_loader import CsvLoader


class TestCliente:
    def test_cliente_creation(self):
        """Test que se puede crear un cliente correctamente"""
        cliente = Cliente(
            id=1,
            nombre="Juan Pérez",
            email="juan@email.com",
            ciudad="Quito",
            edad=30
        )
        assert cliente.id == 1
        assert cliente.nombre == "Juan Pérez"
        assert cliente.email == "juan@email.com"
        assert cliente.ciudad == "Quito"
        assert cliente.edad == 30

    def test_cliente_to_row(self):
        """Test que el método to_row funciona correctamente"""
        cliente = Cliente(
            id=1,
            nombre="Juan Pérez",
            email="juan@email.com",
            ciudad="Quito",
            edad=30
        )
        expected = "1\tJuan Pérez\tjuan@email.com\tQuito\t30"
        assert cliente.to_row() == expected

    def test_cliente_headers(self):
        """Test que los headers son correctos"""
        expected = "id\tnombre\temail\tciudad\tedad"
        assert Cliente.headers() == expected


class TestCustomerManager:
    def test_customer_manager_creation(self):
        """Test que se puede crear un CustomerManager"""
        clientes = [
            Cliente(1, "Juan", "juan@email.com", "Quito", 30),
            Cliente(2, "María", "maria@email.com", "Guayaquil", 25)
        ]
        cm = CustomerManager(clientes)
        assert cm.conteo() == 2

    def test_buscar_por_id(self):
        """Test búsqueda por ID"""
        clientes = [
            Cliente(1, "Juan", "juan@email.com", "Quito", 30),
            Cliente(2, "María", "maria@email.com", "Guayaquil", 25)
        ]
        cm = CustomerManager(clientes)
        
        # Cliente encontrado
        cliente = cm.buscar_por_id(1)
        assert cliente is not None
        assert cliente.nombre == "Juan"
        
        # Cliente no encontrado
        cliente = cm.buscar_por_id(999)
        assert cliente is None

    def test_listar_por_ciudad(self):
        """Test listado por ciudad"""
        clientes = [
            Cliente(1, "Juan", "juan@email.com", "Quito", 30),
            Cliente(2, "María", "maria@email.com", "Guayaquil", 25),
            Cliente(3, "Pedro", "pedro@email.com", "Quito", 35)
        ]
        cm = CustomerManager(clientes)
        
        # Buscar en Quito
        clientes_quito = cm.listar_por_ciudad("Quito")
        assert len(clientes_quito) == 2
        assert all(c.ciudad.lower() == "quito" for c in clientes_quito)
        
        # Buscar en ciudad inexistente
        clientes_inexistente = cm.listar_por_ciudad("CiudadInexistente")
        assert len(clientes_inexistente) == 0

    def test_ordenar_por_edad(self):
        """Test ordenamiento por edad"""
        clientes = [
            Cliente(1, "Juan", "juan@email.com", "Quito", 30),
            Cliente(2, "María", "maria@email.com", "Guayaquil", 25),
            Cliente(3, "Pedro", "pedro@email.com", "Quito", 35)
        ]
        cm = CustomerManager(clientes)
        
        ordenados = cm.ordenar_por_edad()
        edades = [c.edad for c in ordenados]
        assert edades == [25, 30, 35]


class TestCsvLoader:
    def test_csv_loader_creation(self):
        """Test que se puede crear un CsvLoader"""
        loader = CsvLoader("clientes.csv")
        assert loader.ruta_csv == "clientes.csv"
        assert loader.total_leidos == 0
        assert loader.total_validos == 0
        assert loader.total_descartados == 0

    def test_resumen_vacio(self):
        """Test que el resumen inicial es correcto"""
        loader = CsvLoader("clientes.csv")
        resumen = loader.resumen()
        expected = {
            "total_leidos": 0,
            "total_validos": 0,
            "total_descartados": 0
        }
        assert resumen == expected
