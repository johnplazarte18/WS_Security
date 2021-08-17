## WS_Security
Se implementa el web services para smart security system

### 1. Instalar el modulo para encriptar contraseñas
pip install django-fernet-fields

### 2. Instalar el modulo para gestionar imágenes en django
python -m pip install Pillow

### 3. Crear la base de datos con el nombre "security_system"

### 4. Crear las migraciones

### 5. Efectuar las migraciones

### 6. Instalar el framework de Django Rest Framework
pip install djangorestframework

### 7. Insertar datos a partir de fixtures .json

### 8. Instalar el paquete "corsheaders" para el intercambio de recursos y se pueda consumir el web services desde otra aplicación
python -m pip install django-cors-headers

#### Sección 1

Para ejecutar un archivo de restauración de datos es el siguiente comando:
    python manage.py loaddata "nombre del archivo json ubicado dentro de la aplicación django app/fixtures/file.json"

#### Sección 2

Si ya tiene datos en los modelos entonces:

    1. Eliminar los modelos de una app django.
        python manage.py migrate "Nombre de su app django" zero
    2. Migrar los modelos de una app django.
        python manage.py migrate "Nombre de su app django"
    3. Ejecutar el comando antes mencionado en la sección 1 para insertar los datos en el modelo