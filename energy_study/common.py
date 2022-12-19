from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

NRJ_SOURCES = [
    "Fioul",
    "Charbon",
    "Gaz",
    "Nucléaire",
    "Eolien",
    "Solaire",
    "Hydraulique",
    "Pompage",
    "Bioénergies",
    "Ech. physiques",
    "Taux de Co2",
]


FOSSIL_SOURCES = [
    "Fioul",
    "Charbon",
    "Gaz",
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

RENEWABLE_SOURCES = [
    "Eolien",
    "Solaire",
    "Hydraulique",
]
