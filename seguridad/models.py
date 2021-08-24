from django.db import models
from usuario.models import usuarios

class componentes(models.Model):
    nombre = models.CharField(max_length=60)
    sector = models.CharField(max_length=60)
    estado = models.BooleanField()

class historial(models.Model):
    unComponente = models.ForeignKey(componentes, on_delete=models.PROTECT, related_name="componentes")
    fecha = models.DateField()
    # de tipo Anomalía, Solicitado
    tipo = models.CharField(max_length=10)

class evidencias(models.Model):
    unHistorial = models.ForeignKey(historial, on_delete=models.PROTECT, related_name="historial")
    hora = models.TimeField()
    # media/Evidencias
    ruta_foto = models.ImageField(upload_to="Evidencias", null=True, blank=False)

class solicitud(models.Model):
    unUsuario = models.ForeignKey(usuarios, on_delete=models.PROTECT)
    historial_id = models.IntegerField(max_length=7, null=True, blank=True)
    estado = models.BooleanField()
