from django.db import models
from fernet_fields import EncryptedTextField

class usuarios(models.Model):
    nombre = models.CharField(max_length=60)
    rol = models.CharField(max_length=2)
    usuario = models.CharField(max_length=15)
    # campo con clave encriptada
    clave = EncryptedTextField()
    # True= usuario habilitado que puede iniciar sesión, False= deshabilitado
    estado = models.BooleanField()
    # media/Perfiles
    ruta_foto = models.ImageField(upload_to="Perfiles", null=True, blank=False)
    
