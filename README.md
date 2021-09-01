## Web services del sistema de seguridad

## **Instalación**

### Paso 1. Instalar el módulo para encriptar contraseñas
```bash
pip install django-fernet-fields
```

### Paso 2. Instalar el módulo para gestionar imágenes en django
```bash
python -m pip install Pillow
```

### Paso 3. Crear la base de datos con el nombre "security_system" en el gestor de base de datos PostgreSQL, en la versión de su preferencia

### Paso 4. Crear las migraciones
```bash
python manage.py makemigrations
```

### Paso 5. Efectuar las migraciones
```bash
python manage.py migrate
```

### Paso 6. Instalar el framework de Django Rest Framework
```bash
pip install djangorestframework
```

### Paso 7. Insertar datos a partir de los fixtures de .json ubicados dentro de cada aplicación django

##### Sección 1

Para ejecutar un archivo de datos se debe usar el siguiente comando dentro de la ruta: aplicación django/app/fixtures/file.json:
```bash
python manage.py loaddata "nombre del archivo de datos".json
```

##### Sección 2

Si ya tiene datos en ingresados en la base de datos, entonces:

    1. Eliminar el modelo de la app django que ya tiene datos en la base de datos.
        
        python manage.py migrate "Nombre de su app django" zero
        
    2. Migrar el modelo eliminado en la base de datos.
        
        python manage.py migrate "Nombre de su app django"
        
    3. Ejecutar el comando antes mencionado en la sección 1 para insertar los datos en la base de datos.

### Paso 8. Instalar el paquete "corsheaders" para el intercambio de recursos y se pueda consumir el web services desde otra aplicación
```bash
python -m pip install django-cors-headers
```
## **Ejecución**

### En la raíz del proyecto donde se encuentra el archivo manage.py ejecutar el siguiente comando:
```bash
python manage.py runserver
```

### Ahora puede dirigirse a elección de las rutas creadas en los archivos urls.py para acceder a las funcionalidades del web services
```bash
http://127.0.0.1:8000/api-seguridad/historial-anomalias/
```
