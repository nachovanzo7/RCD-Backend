from django.db import models
from obras.models import Obra

class Fotos(models.Model):
    obra = models.ForeignKey(Obra, on_delete=models.CASCADE, related_name='imagenes_set')
    imagen = models.ImageField(upload_to='obras/imagenes/')
    descripcion = models.TextField("Descripción", blank=True, null=True)
    fecha = models.DateField("Fecha", blank=True, null=True)

    def __str__(self):
        return f"Imagen de {self.obra.nombre_obra}"
