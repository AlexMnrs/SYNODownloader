"""
    .SYNOPSIS
        Cliente API para interactuar con Synology FileStation.

    .DESCRIPTION
        Este módulo contiene la clase SynologyClient, que gestiona la autenticación,
        el listado de archivos y la descarga de contenidos desde un NAS Synology
        utilizando la API de FileStation.

    .NOTES
        Script Name: client.py
        Author:      Alex Monrás
        Created:     2026-01-22
        Version:     1.1.0
"""

import requests
import os
from pathlib import Path
from typing import Dict, List, Optional, Any
from tqdm import tqdm
import time

class SynologyClient:
    def __init__(self, url: str, user: str, password: str, download_path: str):
        self.url = url
        self.user = user
        self.password = password
        self.download_path = Path(download_path)
        self.sid: Optional[str] = None
        self.session = requests.Session()

    def login(self) -> bool:
        """Autentica con el NAS de Synology."""
        try:
            params = {
                'api': 'SYNO.API.Auth',
                'version': 3,
                'method': 'login',
                'account': self.user,
                'passwd': self.password,
                'session': 'FileStation',
                'format': 'cookie'
            }
            response = self.session.get(self.url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if data.get('success'):
                self.sid = data['data']['sid']
                return True
            else:
                print(f"Inicio de sesión fallido: {data}")
                return False
        except Exception as e:
            print(f"Error de inicio de sesión: {e}")
            return False

    def list_files(self, remote_path: str) -> Dict[int, str]:
        """Lista archivos en un directorio remoto, excluyendo subdirectorios."""
        if not self.sid:
            raise Exception("No hay sesión iniciada")

        # Asegurar que la ruta remota comience con /
        if not remote_path.startswith("/"):
            remote_path = "/" + remote_path

        params = {
            'api': 'SYNO.FileStation.List',
            'version': 2,
            'method': 'list',
            'additional': '',
            'folder_path': remote_path,
            '_sid': self.sid
        }
        
        try:
            response = self.session.get(self.url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if not data.get('success'):
                print(f"Fallo al listar archivos: {data}")
                return {}

            files = data['data']['files']
            file_map = {}
            index = 1
            for file in files:
                if not file.get('isdir'):
                    file_map[index] = file['name']
                    index += 1
            
            return file_map
        except Exception as e:
            print(f"Error al listar archivos: {e}")
            return {}

    def download_file(self, remote_path: str, filename: str) -> bool:
        """Descarga un archivo mostrando una barra de progreso."""
        if not self.sid:
            raise Exception("No hay sesión iniciada")
            
        full_remote_path = f"/{remote_path.strip('/')}/{filename}"
        local_file_path = self.download_path / filename

        # Crear directorio de descarga si no existe
        self.download_path.mkdir(parents=True, exist_ok=True)

        params = {
            'api': 'SYNO.FileStation.Download',
            'version': 2,
            'method': 'download',
            'path': full_remote_path,
            'mode': 'open',
            '_sid': self.sid
        }

        try:
            with self.session.get(self.url, params=params, stream=True) as r:
                r.raise_for_status()
                total_size = int(r.headers.get('content-length', 0))
                
                with open(local_file_path, 'wb') as f, tqdm(
                    desc=filename,
                    total=total_size,
                    unit='iB',
                    unit_scale=True,
                    unit_divisor=1024,
                ) as bar:
                    for chunk in r.iter_content(chunk_size=8192):
                        size = f.write(chunk)
                        bar.update(size)
            return True
        except Exception as e:
            print(f"Error de descarga: {e}")
            # Limpiar archivo parcial
            if local_file_path.exists():
                local_file_path.unlink()
            return False

    def logout(self):
        """Cierra la sesión actual."""
        if not self.sid:
            return

        try:
            params = {
                'api': 'SYNO.API.Auth',
                'version': 1,
                'method': 'logout',
                'session': 'FileStation'
            }
            self.session.get(self.url, params=params)
            self.sid = None
        except Exception:
            pass
