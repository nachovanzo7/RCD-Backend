from django.db import models
from visitas.models import Visita

class Fotos(models.Model):
    id = models.AutoField(primary_key=True)
    ubicacion_server = models.CharField(max_length=200)
    tipo_imagen = models.CharField(max_length=200)
    visita = models.ForeignKey(Visita, on_delete=models.CASCADE, related_name='visitas')
