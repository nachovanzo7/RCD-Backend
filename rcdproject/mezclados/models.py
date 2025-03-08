from django.db import models
from django.core.validators import FileExtensionValidator
from obras.models import Obra

class Mezclado(models.Model):
    obra = models.ForeignKey(Obra, on_delete=models.CASCADE, related_name="mezclados")
    pesaje = models.DecimalField("Pesaje", max_digits=10, decimal_places=2)
    fecha_registro = models.DateTimeField("Fecha de Registro", auto_now_add=True)

    def __str__(self):
        return f"Mezclado de {self.obra.nombre_obra} - Pesaje: {self.pesaje}"

class MezcladoImagen(models.Model):
    mezclado = models.ForeignKey(Mezclado, on_delete=models.CASCADE, related_name="imagenes")
    imagen = models.ImageField(
        "Imagen",
        upload_to="mezclados/",
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'png', 'jpeg'])]
    )
    fecha_subida = models.DateTimeField("Fecha de Subida", auto_now_add=True)

    def __str__(self):
        return f"Imagen de {self.mezclado}"
