from __future__ import annotations
from typing import List, Optional
from .models import Cliente


class CustomerManager:
    def __init__(self, clientes: List[Cliente]):
        self._clientes = list(clientes)

    def conteo(self) -> int:
        return len(self._clientes)

    def buscar_por_id(self, cid: int) -> Optional[Cliente]:
        if not isinstance(cid, int):
            return None
        for c in self._clientes:
            if c.id == cid:
                return c
        return None

    def listar_por_ciudad(self, ciudad: str) -> List[Cliente]:
        ciudad_norm = (ciudad or "").strip().lower()
        if not ciudad_norm:
            return []
        return [c for c in self._clientes if c.ciudad.strip().lower() == ciudad_norm]

    def ordenar_por_edad(self) -> List[Cliente]:
        # Orden estable: edad asc, empate por id
        return sorted(self._clientes, key=lambda c: (c.edad, c.id))
