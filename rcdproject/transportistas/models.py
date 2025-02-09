from django.db import models

class Transportista(models.Model):
    TIPOS_MATERIAL_CHOICES = [
        ('escombro_limpio', 'Escombro Limpio'),
        ('plastico', 'Plástico'),
        ('papel_carton', 'Papel y Cartón'),
        ('metales', 'Metales'),
        ('madera', 'Madera'),
        ('mezclados', 'Mezclados'),
        ('peligrosos', 'Peligrosos'),
    ]
    
    nombre = models.CharField(max_length=200)
    contacto = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    tipo_vehiculo = models.CharField(max_length=100)
    tipo_material = models.CharField(max_length=20, choices=TIPOS_MATERIAL_CHOICES)
