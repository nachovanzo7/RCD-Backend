from django.db import models
from obras.models import Obra

class SupervisorObra(models.Model):
    NIVEL_CAPACITACION_CHOICES = [
        ('participa_activamente', 'Participa Activamente'),
        ('participa_pero_puede_mejorar', 'Participa Pero Puede Mejorar'),
        ('poca_participacion', 'Poca Participacion'),
        ('falta_mayor_participacion', 'Falta Mayor Participacion'),
        ('no_participa', 'No Participa'),
        ('no_hay', 'No Hay'),
    ]
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    telefono = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    obra = models.OneToOneField(Obra, on_delete=models.CASCADE, related_name='supervisor')
    nivel_capacitacion = models.CharField(max_length=50, choices=NIVEL_CAPACITACION_CHOICES, default='No Hay')
