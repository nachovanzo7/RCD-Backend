from django.db import models
from obras.models import Obra
from tecnicos.models import Tecnico

class Capacitacion(models.Model):
    id = models.AutoField(primary_key=True)
    fecha = models.DateField("Fecha de Capacitacion")
    motivo = models.CharField("Motivo", max_length=200)
    obra = models.ForeignKey(Obra, on_delete=models.CASCADE, related_name='capacitaciones', verbose_name="Obra")
    tecnico = models.ForeignKey(Tecnico, on_delete=models.CASCADE, related_name='capacitaciones', verbose_name="Técnico")
    comentario = models.TextField("Comentario", blank=True, null=True)
 