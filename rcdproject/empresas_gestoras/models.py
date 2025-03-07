# empresas_gestoras/models.py
from django.db import models

class EmpresaGestora(models.Model):
    TIPOS_MATERIAL_CHOICES = [
        ('escombro_limpio', 'Escombro Limpio'),
        ('plastico', 'Plástico'),
        ('papel_carton', 'Papel y Cartón'),
        ('metales', 'Metales'),
        ('madera', 'Madera'),
        ('mezclados', 'Mezclados'),
        ('peligrosos', 'Peligrosos'),
    ]

    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=200)
    ubicacion = models.CharField(max_length=200)
    contacto = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    tipo_material = models.CharField(
        max_length=20,
        choices=TIPOS_MATERIAL_CHOICES,
        default='plastico'
    )

    def __str__(self):
        return self.nombre
