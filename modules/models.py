from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Cliente:
    id: int
    nombre: str
    email: str
    ciudad: str
    edad: int

    def to_row(self) -> str:
        return f"{self.id}\t{self.nombre}\t{self.email}\t{self.ciudad}\t{self.edad}"

    @staticmethod
    def headers() -> str:
        return "id\tnombre\temail\tciudad\tedad"
