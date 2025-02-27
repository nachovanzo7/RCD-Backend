from django.db import models
from obras.models import Obra

class CondicionDeObra(models.Model):
    obra = models.ForeignKey(Obra, on_delete=models.CASCADE, related_name='condiciones_de_obra')
    jornal_ambiental = models.TextField()
    operarios = models.TextField()
    oficina_tecnica = models.TextField()
    participantes_de_obra_observaciones = models.TextField()
    limpieza_general_por_terreno = models.TextField()
    limpieza_general_por_pisos = models.TextField()
    limpieza_general_observaciones = models.TextField()
    logistica_de_obra = models.TextField()
    logistica_de_obra_observaciones = models.TextField()
