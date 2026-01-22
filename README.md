# SYNODownloader

![Version](https://img.shields.io/badge/version-1.1.0-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)

Esta aplicación permite descargar archivos desde un NAS de Synology utilizando la API de FileStation. Está diseñada para ser simple, segura y eficiente, permitiendo navegar por los directorios remotos y descargar archivos seleccionados con una barra de progreso visual.

## 🚀 Características

- **Autenticación Segura**: Utiliza la API oficial de Synology (Auth API v3).
- **Navegación Remota**: Lista archivos de directorios remotos del NAS.
- **Barra de Progreso**: Visualización moderna del progreso de descarga (usando `tqdm`).
- **Seguridad**: Gestión de credenciales mediante variables de entorno (`.env`), evitando contraseñas en código.
- **Multiplataforma**: Funciona en Windows, Linux y macOS.

## 📋 Requisitos Previos

- Python 3.8 o superior.
- Acceso a un NAS Synology con FileStation habilitado.
- (Opcional) Entorno virtual configurado.

## 🛠️ Instalación

1. **Clonar el repositorio**:
   ```bash
   git clone https://github.com/alexmnrs/SYNODownloader.git
   cd SYNODownloader
   ```

2. **Crear y activar un entorno virtual** (Recomendado):
   ```bash
   # Windows
   python -m venv .venv
   .venv\Scripts\activate
   
   # Linux/macOS
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

## ⚙️ Configuración

1. Duplica el archivo de ejemplo de configuración:
   ```bash
   cp .env.example .env
   # O en Windows: copy .env.example .env
   ```

2. Edita el archivo `.env` con tus credenciales y configuración:
   ```ini
   SYNO_URL="https://tu-nas.com:5001/webapi/entry.cgi"
   SYNO_USER="tu_usuario"
   SYNO_PASSWORD="tu_password"
   DOWNLOAD_PATH="Downloads"
   ```

## 💻 Uso

Ejecuta el script principal:

```bash
python main.py
```

Sigue las instrucciones en pantalla:
1. El script verificará la conexión.
2. Ingresa la ruta remota que deseas explorar (por defecto `/`).
3. Selecciona el número del archivo que deseas descargar.

## 📂 Estructura del Proyecto

```
SYNODownloader/
├── src/
│   ├── client.py    # Lógica de conexión y API de Synology
│   └── config.py    # Gestión de configuración y validación
├── .env.example     # Plantilla de variables de entorno
├── .gitignore       # Archivos ignorados por Git
├── LICENSE          # Licencia del proyecto
├── main.py          # Punto de entrada de la aplicación
├── README.md        # Documentación
└── requirements.txt # Dependencias del proyecto
```

## 🤝 Contribución

Las contribuciones son bienvenidas. Por favor, abre un issue primero para discutir qué te gustaría cambiar.

## 📄 Licencia

[MIT](LICENSE)

## ✍️ Autor

**Alex Monrás**
- GitHub: [@alexmnrs](https://github.com/alexmnrs)
