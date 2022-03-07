# 1.0.0

Esta aplicación permite descargar archivos de un NAS de la marca Synology, concretamente de la herramienta de administración de archivos FileStation (probado con el DS218Play).

### Paso 1: Instalar los requerimientos

```
$ pip install -r requirements.txt
```

### Paso 2: Configurar las variables

Antes de ejecutar el programa debes modificar las variables que contienen los datos de acceso a tu NAS de Synology.

```
URL  =  'https://nas.quickconnect.to:65375/'
USER =  'admin'
PASS =  'password'
PATH =  'videos'
```

### Paso 3: Ejecutar el programa

Al ejecutar el programa te pedirá que elijas una carpeta donde descargar los archivos. Si la carpeta existe, te preguntará si quieres utilizarla. Si no existe, la creará. 

Una vez configurada la carpeta de descargas, imprimirá en una lista de todos los archivos del NAS.

Selecciona el archivo a descargar introduciendo el número correspondiente.

Espera a que se descargue y finalice el programa automáticamente.

### Known Issues

- Cuando termina la descarga el porcentaje de completado no es 100%.
