"""
    .SYNOPSIS
        Script principal para la descarga de archivos desde Synology NAS.

    .DESCRIPTION
        Este script orquesta el flujo de la aplicación: carga la configuración,
        autentica al usuario, lista los archivos disponibles en el directorio remoto
        y permite al usuario seleccionar archivos para descargar.

    .NOTES
        Script Name: main.py
        Author:      Alex Monrás
        Created:     2026-01-22
        Version:     1.1.0
"""

import sys
import os
from src.config import Config
from src.client import SynologyClient

def main():
    # Limpiar pantalla (compatible multiplataforma)
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Validar configuración
    error = Config.validate()
    if error:
        print(f"Error de Configuración: {error}")
        print("Por favor verifica tu archivo .env.")
        sys.exit(1)

    print("[*] Inicializando SYNODownloader...")
    
    client = SynologyClient(
        url=Config.SYNO_URL,
        user=Config.SYNO_USER,
        password=Config.SYNO_PASSWORD,
        download_path=Config.DOWNLOAD_PATH
    )

    try:
        print("[*] Iniciando sesión...")
        if not client.login():
            print("[!] Fallo en el inicio de sesión. Verifica las credenciales.")
            sys.exit(1)
        
        print("[+] Inicio de sesión exitoso.")
        
        # Solicitar ruta remota o usar raíz por defecto
        remote_path = input("[?] Introduce la ruta remota a listar (por defecto: /): ").strip() or "/"
        
        print(f"[*] Listando archivos en {remote_path}...")
        files = client.list_files(remote_path)
        
        if not files:
            print("[!] No se encontraron archivos o acceso denegado.")
        else:
            print("\nArchivos disponibles:")
            for index, filename in files.items():
                print(f"[{index}] {filename}")
            
            while True:
                try:
                    choice_input = input("\n[*] Elige un número de archivo (o 'q' para salir): ")
                    if choice_input.lower() == 'q':
                        break
                        
                    choice = int(choice_input)
                    if choice in files:
                        filename = files[choice]
                        confirm = input(f"[*] ¿Descargar '{filename}'? (y/n): ")
                        if confirm.lower() == 'y':
                            print(f"[*] Descargando {filename}...")
                            if client.download_file(remote_path, filename):
                                print(f"[+] Descargado exitosamente en {client.download_path}")
                            else:
                                print("[!] Falló la descarga.")
                    else:
                        print("[!] Selección inválida.")
                except ValueError:
                    print("[!] Por favor introduce un número.")

    except KeyboardInterrupt:
        print("\n\n[*] Operación interrumpida por el usuario.")
    except Exception as e:
        print(f"\n[!] Ocurrió un error inesperado: {e}")
    finally:
        print("[*] Cerrando sesión...")
        client.logout()

if __name__ == '__main__':
    main()