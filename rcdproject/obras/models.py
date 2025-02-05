from django.db import models
from clientes.models import Cliente

class Obra(models.Model):
    id = models.AutoField(primary_key=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='obras')
    nombre = models.CharField(max_length=200)
    direccion = models.CharField(max_length=200)
    metros_cuadrados = models.DecimalField(max_digits=10, decimal_places=3)
    imagenes = models.ImageField(upload_to='obras/imagenes/', null=True, blank=True)

class SolicitudObra(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('aceptado', 'Aceptado'),
        ('rechazado', 'Rechazado'),
    ]
    obra = models.OneToOneField(Obra, on_delete=models.CASCADE, related_name='solicitud', primary_key=True)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='pendiente')
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
