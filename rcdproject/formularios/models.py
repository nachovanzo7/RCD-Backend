from django.db import models
from tecnicos.models import Tecnico
from obras.models import Obra

class Formularios(models.Model):
    id = models.AutoField(primary_key=True)
    tecnico = models.ForeignKey(Tecnico, on_delete=models.CASCADE, related_name='formularios', blank=True, null=True)
    obra = models.ForeignKey(Obra, on_delete=models.CASCADE, related_name='formularios', blank=True, null=True)
    fecha = models.DateField("Fecha", blank=True, null=True)

    motivo_de_visita = models.CharField("Motivo de visita", max_length=200, blank=True, null=True)
    otro_motivo = models.CharField("Otro motivo", max_length=200, blank=True, null=True)

    participante_jornal_ambiental = models.CharField("Participante jornal ambiental", max_length=200, blank=True, null=True)
    participante_operario = models.CharField("Participante operario", max_length=200, blank=True, null=True)
    participante_oficina_tecnica = models.CharField("Participante oficina técnica", max_length=200, blank=True, null=True)
    participante_observaciones = models.CharField("Participante observaciones", max_length=500, blank=True, null=True)

    limpieza_general_en_terreno = models.CharField("Limpieza general en terreno", max_length=200, blank=True, null=True)
    limpieza_general_en_pisos = models.CharField("Limpieza general en pisos", max_length=200, blank=True, null=True)
    limpieza_general_observaciones = models.CharField("Limpieza observaciones", max_length=500, blank=True, null=True)

    logistica_de_obra = models.CharField("Logística de obra", max_length=200, blank=True, null=True, default="No especificado")
    logistica_de_obra_observaciones = models.CharField("Logística observaciones", max_length=500, blank=True, null=True)

    PUNTOLIMPIO_CHOICES = [('si_hay', 'Sí Hay'), ('no_hay', 'No Hay')]
    punto_limpio = models.CharField("Punto limpio", max_length=200, choices=PUNTOLIMPIO_CHOICES, blank=True, null=True, default="no_hay")
    punto_limpio_ubicacion = models.CharField("Punto limpio ubicación", max_length=200, blank=True, null=True, default="No especificado")
    punto_limpio_estructura = models.CharField("Punto limpio estructura", max_length=200, blank=True, null=True, default="No especificado")
    punto_limpio_tipo_contenedor = models.CharField("Punto limpio tipo contenedor", max_length=200, blank=True, null=True, default="No especificado")
    punto_limpio_estado_contenedor = models.CharField("Punto limpio estado", max_length=200, blank=True, null=True, default="No especificado")
    punto_limpio_señaletica = models.CharField("Punto limpio señalética", max_length=200, blank=True, null=True, default="No especificado")
    punto_limpio_observaciones = models.CharField("Punto limpio observaciones", max_length=500, blank=True, null=True)

    HAY_TIPO_MATERIAL_CHOICES = [('Aplica', 'Aplica'), ('no_aplica', 'No Aplica')]
    escombro_limpio = models.CharField("Escombro limpio", max_length=200, choices=HAY_TIPO_MATERIAL_CHOICES, blank=True, null=True, default="no_aplica")
    plastico = models.CharField("Plástico", max_length=200, choices=HAY_TIPO_MATERIAL_CHOICES, blank=True, null=True, default="no_aplica")
    papel_y_carton = models.CharField("Papel y cartón", max_length=200, choices=HAY_TIPO_MATERIAL_CHOICES, blank=True, null=True, default="no_aplica")
    metales = models.CharField("Metales", max_length=200, choices=HAY_TIPO_MATERIAL_CHOICES, blank=True, null=True, default="no_aplica")
    madera = models.CharField("Madera", max_length=200, choices=HAY_TIPO_MATERIAL_CHOICES, blank=True, null=True, default="no_aplica")
    mezclados = models.CharField("Mezclados", max_length=200, choices=HAY_TIPO_MATERIAL_CHOICES, blank=True, null=True, default="no_aplica")
    peligrosos = models.CharField("Peligrosos", max_length=200, choices=HAY_TIPO_MATERIAL_CHOICES, blank=True, null=True, default="no_aplica")
    otras_observaciones = models.CharField("Otras observaciones", max_length=500, blank=True, null=True)
    acciones_tomadas = models.CharField("Acciones tomadas", max_length=500, blank=True, null=True)  # ✅ Agregado
