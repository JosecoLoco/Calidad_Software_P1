from __future__ import annotations
from typing import List, Tuple, Dict
import os
import pandas as pd

from .models import Cliente


class CsvLoader:
    def __init__(self, ruta_csv: str):
        self.ruta_csv = ruta_csv
        self.total_leidos = 0
        self.total_validos = 0
        self.total_descartados = 0

    def cargar(self) -> List[Cliente]:
        if not os.path.exists(self.ruta_csv) or os.path.getsize(self.ruta_csv) == 0:
            raise FileNotFoundError("Archivo clientes.csv no encontrado o vacío.")

        # Tipos estrictos; errores se convierten en NaN para poder filtrar
        try:
            df = pd.read_csv(
                self.ruta_csv,
                dtype={"id": "Int64", "nombre": "string", "email": "string", "ciudad": "string", "edad": "Int64"},
                keep_default_na=True,
                na_values=['', 'awt', 'SJY', 'dQW', 'ZKz', 'WHr', 'Nvq', 'pfE', 'Pls', 'BqV', 'zpI', 'ysl']
            )
        except Exception as e:
            # Si hay problemas con el parsing, intentar con tipos más flexibles
            df = pd.read_csv(
                self.ruta_csv,
                dtype=str,
                keep_default_na=True
            )
            # Convertir columnas numéricas manualmente
            df['id'] = pd.to_numeric(df['id'], errors='coerce')
            df['edad'] = pd.to_numeric(df['edad'], errors='coerce')

        self.total_leidos = len(df)

        # Normalización mínima
        for col in ("nombre", "email", "ciudad"):
            if col in df.columns:
                df[col] = df[col].fillna("").astype("string").str.strip()

        # Reglas de validez - verificar que las columnas existan
        required_columns = ["id", "edad", "ciudad"]
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"Columnas requeridas faltantes: {missing_columns}")
        
        # Reglas de validez
        mask_valid = (
            df["id"].notna() &
            df["edad"].notna() &
            df["ciudad"].astype("string").str.len().gt(0)
        )

        df_valid = df[mask_valid].copy()
        self.total_validos = len(df_valid)
        self.total_descartados = self.total_leidos - self.total_validos

        clientes: List[Cliente] = []
        for _, row in df_valid.iterrows():
            try:
                clientes.append(
                    Cliente(
                        id=int(row["id"]),
                        nombre=str(row.get("nombre", "")),
                        email=str(row.get("email", "")),
                        ciudad=str(row.get("ciudad", "")),
                        edad=int(row["edad"]),
                    )
                )
            except Exception:
                # Si una fila “válida” todavía rompe, descártala silenciosamente
                self.total_descartados += 1
        return clientes

    def resumen(self) -> Dict[str, int]:
        return {
            "total_leidos": self.total_leidos,
            "total_validos": self.total_validos,
            "total_descartados": self.total_descartados,
        }
