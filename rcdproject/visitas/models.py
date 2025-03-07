from django.db import models
from obras.models import Obra
from tecnicos.models import Tecnico

class Visita(models.Model):
    id = models.AutoField(primary_key=True)
    obra = models.ForeignKey(Obra, on_delete=models.CASCADE, related_name='visitas', verbose_name="Obra")
    tecnico = models.ForeignKey(Tecnico, on_delete=models.CASCADE, related_name='visitas', verbose_name="Técnico")
    fecha = models.DateField("Fecha de Visita")
    motivo = models.CharField("Motivo", max_length=200)
    observaciones = models.TextField("Observaciones", blank=True, null=True)
    acciones_tomadas = models.TextField("Acciones tomadas", blank=True, null=True)

    def __str__(self):
        return f"Visita {self.id}"
