# 1.0.0

Esta aplicación permite descargar archivos de un NAS de la marca Synology, concretamente de la herramienta de administración de archivos FileStation (probado con el DS218Play).

### Paso 1: Instalar los requerimientos

```
$ pip install -r requirements.txt
```

### Paso 2: Configurar las variables

Antes de ejecutar el programa debes modificar tus datos en el archivo credentials.py.

```
URL  =  'https://nas.quickconnect.to:65375/'
USER =  'admin'
PASS =  'password'
PATH =  'videos'
```

### Paso 3: Ejecutar el programa

```
$ python main.py
```

### Problemas conocidos

- Cuando termina la descarga el porcentaje de completado no es 100%.
- Error al descargar archivos que contienen caracteres especiales en el nombre (el símbolo de la suma (+))
