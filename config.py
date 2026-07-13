import os
import secrets


class Config:
    """
    Configuració general de Missions
    """

    # Carpeta arrel del projecte
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    # Base de dades SQLite
    DATABASE = os.path.join(BASE_DIR, "data", "missions.db")

    # Clau de sessió de Flask
    SECRET_KEY = secrets.token_hex(32)

    # Configuració Flask
    DEBUG = True

    # Configuració futura
    APP_NAME = "Missions"
    VERSION = "0.1.0"

    # Idioma
    LANGUAGE = "ca"

    # Zona horària
    TIMEZONE = "Europe/Madrid"

    # Gamificació
    DEFAULT_POINTS = 10

    # PWA (més endavant)
    PWA_NAME = "Missions"
    PWA_SHORT_NAME = "Missions"