"""
    .SYNOPSIS
        Gestiona la configuración de la aplicación cargando variables de entorno.

    .DESCRIPTION
        Este módulo define la clase Config, encargada de leer y validar las variables
        de entorno necesarias para la conexión con el NAS de Synology.
        Utiliza python-dotenv para cargar configuraciones desde un archivo .env.

    .NOTES
        Script Name: config.py
        Author:      Alex Monrás
        Created:     2026-01-22
        Version:     1.1.0
"""

import os
from dotenv import load_dotenv
from typing import Optional

# Cargar variables de entorno desde el archivo .env
load_dotenv()

class Config:
    SYNO_URL: str = os.getenv("SYNO_URL", "")
    SYNO_USER: str = os.getenv("SYNO_USER", "")
    SYNO_PASSWORD: str = os.getenv("SYNO_PASSWORD", "")
    DOWNLOAD_PATH: str = os.getenv("DOWNLOAD_PATH", "Downloads")

    @classmethod
    def validate(cls) -> Optional[str]:
        """Valida que todas las variables de configuración requeridas estén establecidas."""
        if not cls.SYNO_URL:
            return "SYNO_URL no está configurado en el entorno o archivo .env."
        if not cls.SYNO_USER:
            return "SYNO_USER no está configurado en el entorno o archivo .env."
        if not cls.SYNO_PASSWORD:
            return "SYNO_PASSWORD no está configurado en el entorno o archivo .env."
        return None
