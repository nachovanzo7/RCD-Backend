from django.db import models
from obras.models import Obra

from django.contrib.auth import get_user_model
Usuario = get_user_model()


class SupervisorObra(models.Model):
    NIVEL_CAPACITACION_CHOICES = [
        ('participa_activamente', 'Participa Activamente'),
        ('participa_pero_puede_mejorar', 'Participa Pero Puede Mejorar'),
        ('poca_participacion', 'Poca Participacion'),
        ('falta_mayor_participacion', 'Falta Mayor Participacion'),
        ('no_participa', 'No Participa'),
        ('no_hay', 'No Hay'),
    ]
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='supervisor', null=True, blank=True)
    telefono = models.CharField(max_length=50)
    obra = models.OneToOneField(Obra, on_delete=models.CASCADE, related_name='supervisor')
    nivel_capacitacion = models.CharField(max_length=50, choices=NIVEL_CAPACITACION_CHOICES, default='no_hay')
