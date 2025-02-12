from django.db import models
from obras.models import Obra


class PuntoLimpio(models.Model):
    obra = models.ForeignKey(Obra, on_delete=models.CASCADE, related_name='puntos_limpios')
    ubicacion = models.CharField("Ubicación", max_length=200)
    cantidad = models.IntegerField("Cantidad")
    metros_cuadrados = models.DecimalField("Metros Cuadrados", max_digits=10, decimal_places=2)
    estructura = models.CharField("Estructura", max_length=200)
    tipo_contenedor = models.CharField("Tipo de Contenedor", max_length=200)
    puntaje = models.IntegerField("Puntaje")
    señaletica = models.BooleanField("Señalética", default=True)
    observaciones = models.TextField("Observaciones", blank=True, null=True)
    clasificacion = models.CharField("Clasificación", max_length=100)
