from typing import Iterable, Dict
from .models import Cliente


def print_cliente(c: Cliente) -> None:
    print(Cliente.headers())
    print(c.to_row())


def print_lista(lst: Iterable[Cliente]) -> None:
    lst = list(lst)
    if not lst:
        print("(sin resultados)")
        return
    print(Cliente.headers())
    for c in lst:
        print(c.to_row())


def print_resumen(res: Dict[str, int]) -> None:
    print("Resumen de carga")
    for k, v in res.items():
        print(f"- {k}: {v}")


def print_error(msg: str) -> None:
    print(f"[ERROR] {msg}")


def print_info(msg: str) -> None:
    print(f"[INFO] {msg}")
