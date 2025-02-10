from django.db import models
from obras.models import Obra

class SupervisorObra(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    telefono = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    obra = models.OneToOneField(Obra, on_delete=models.CASCADE, related_name='supervisor')

