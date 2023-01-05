from pathlib import Path
import inspect
import re

BASE_DIR = Path(__file__).resolve().parent


def calculated_field(function):
    def wrapper(x):
        x.is_calculated_field = True
        return x

    return wrapper


class DataColumnSpec:
    FUEL_OIL = "Fioul"
    COAL = "Charbon"
    GAZ = "Gaz"
    NUCLEAR = "Nucléaire"
    WIND = "Eolien"
    SOLAR = "Solaire"
    HYDRAULIC = "Hydraulique"
    PUMPED_STORAGE = "Pompage"
    BIO_ENERGY = "Bioénergies"
    EXCHANGE = "Ech. physiques"

    CONSUMPTION = "Consommation"
    FORECAST = "Prévision_J_1"

    ENERGY_SOURCES = [
        FUEL_OIL,
        COAL,
        GAZ,
        NUCLEAR,
        WIND,
        SOLAR,
        HYDRAULIC,
        PUMPED_STORAGE,
        BIO_ENERGY,
        EXCHANGE,
    ]

    FOSSIL_SOURCES = [
        FUEL_OIL,
        COAL,
        GAZ,
    ]

    RENEWABLE_SOURCES = [
        WIND,
        SOLAR,
        HYDRAULIC,
    ]

    @classmethod
    def PREVISION_ERROR(cls):
        return f"{cls.CONSUMPTION}-{cls.FORECAST}"

    @classmethod
    def mappings(cls):
        attributes = inspect.getmembers(
            cls, lambda a: not (inspect.isroutine(a)) and isinstance(a, str)
        )
        return {
            a[1]: a[0]
            for a in attributes
            if not (a[0].startswith("__") and a[0].endswith("__"))
        }

    @classmethod
    def calculated_field_mappings(cls):
        attributes = inspect.getmembers(cls, lambda a: inspect.isroutine(a))
        return [
            a[0]
            for a in attributes
            if not (a[0].startswith("__") and a[0].endswith("__"))
            and re.search("[^a-z]{2}", a[0])
        ]


NRJ_DETAILED_SOURCES = [
    "Ech. comm. Angleterre",
    "Ech. comm. Espagne",
    "Ech. comm. Italie",
    "Ech. comm. Suisse",
    "Ech. comm. Allemagne-Belgique",
    "Fioul - TAC",
    "Fioul - Cogén.",
    "Fioul - Autres",
    "Gaz - TAC",
    "Gaz - Cogén.",
    "Gaz - CCG",
    "Gaz - Autres",
    "Hydraulique - Fil de l?eau + éclusée",
    "Hydraulique - Lacs",
    "Hydraulique - STEP turbinage",
    "Bioénergies - Déchets",
    "Bioénergies - Biomasse",
    "Bioénergies - Biogaz",
]
