# 1.0.0

Esta aplicación permite descargar archivos de un NAS de la marca Synology, concretamente de la herramienta de administración de archivos FileStation (probado con el DS218Play).

### Paso 1: Instalar los requerimientos

```
$ pip install -r requirements.txt
```

### Paso 2: Configurar las variables

```
URL = 'CHANGE_THIS'     # URL DE TU NAS
USER = 'CHANGE_THIS'    # USUARIO
PASS = 'CHANGE_THIS'    # CONTRASEÑA
PATH = 'CHANGE_THIS'    # RUTA DE LA CARPETA
```

### Paso 3: Ejecutar el programa

Al ejecutar el programa se imprimirá en consola una lista de todos los archivos de la carpeta seleccionada.

Selecciona el archivo a descargar introduciendo el número que le corresponda.

El archivo se guardará en la raíz de la carpeta donde se encuentra el script.
