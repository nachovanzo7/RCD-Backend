from django.db import models
from rcdproject.clientes.models import Cliente

class Notificacion(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='notificaciones')
    mensaje = models.CharField("Mensaje", max_length=500)
    created_at = models.DateTimeField("Fecha de creacion", auto_now_add=True)