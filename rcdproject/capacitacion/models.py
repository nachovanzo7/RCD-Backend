# capacitacion/models.py (o donde definas tu modelo Capacitacion)
from django.db import models
from obras.models import Obra
from tecnicos.models import Tecnico
from supervisor_obra.models import SupervisorObra  # Ajusta la ruta según tu estructura

class Capacitacion(models.Model):
    id = models.AutoField(primary_key=True)
    fecha = models.DateField("Fecha de Capacitacion")
    motivo = models.CharField("Motivo", max_length=200)
    obra = models.ForeignKey(Obra, on_delete=models.CASCADE, related_name='capacitaciones', verbose_name="Obra")
    tecnico = models.ForeignKey(Tecnico, on_delete=models.CASCADE, related_name='capacitaciones', verbose_name="Técnico")
    comentario = models.TextField("Comentario", blank=True, null=True)

    supervisor = models.ForeignKey(
        SupervisorObra,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
        
    )


    def __str__(self):
        return f"{self.motivo} - {self.fecha}"
