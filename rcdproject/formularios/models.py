# models.py
from django.db import models
from tecnicos.models import Tecnico
from obras.models import Obra

class Formularios(models.Model):
    id = models.AutoField(primary_key=True)
    tecnico = models.ForeignKey(Tecnico, on_delete=models.CASCADE, related_name='formularios', blank=True, null=True)
    obra = models.ForeignKey(Obra, on_delete=models.CASCADE, related_name='formularios', blank=True, null=True)
    fecha = models.DateField("Fecha", blank=True, null=True)

    # Página 1
    motivo_de_visita = models.CharField("Motivo de visita", max_length=200, blank=True, null=True)
    otro_motivo = models.CharField("Otro motivo", max_length=200, blank=True, null=True)

    # Página 2
    participante_jornal_ambiental = models.CharField("Participante jornal ambiental", max_length=200, blank=True, null=True)
    participante_operario = models.CharField("Participante operario", max_length=200, blank=True, null=True)
    participante_oficina_tecnica = models.CharField("Participante oficina técnica", max_length=200, blank=True, null=True)
    participante_observaciones = models.CharField("Participante observaciones", max_length=500, blank=True, null=True)
    limpieza_general_en_terreno = models.CharField("Limpieza general en terreno", max_length=200, blank=True, null=True)
    limpieza_general_en_pisos = models.CharField("Limpieza general en pisos", max_length=200, blank=True, null=True)
    limpieza_general_observaciones = models.CharField("Limpieza observaciones", max_length=500, blank=True, null=True)
    logistica_de_obra = models.CharField("Logística de obra", max_length=200, blank=True, null=True, default="No especificado")
    logistica_de_obra_observaciones = models.CharField("Logística observaciones", max_length=500, blank=True, null=True)

    # Página 3 (Punto Limpio)
    PUNTOLIMPIO_CHOICES = [('Hay', 'Hay'), ('No Hay', 'No Hay')]
    punto_limpio = models.CharField("Punto limpio", max_length=200, choices=PUNTOLIMPIO_CHOICES, blank=True, null=True, default="No Hay")
    punto_limpio_ubicacion = models.CharField("Punto limpio ubicación", max_length=200, blank=True, null=True, default="No especificado")
    punto_limpio_estructura = models.CharField("Punto limpio estructura", max_length=200, blank=True, null=True, default="No especificado")
    punto_limpio_tipo_contenedor = models.CharField("Punto limpio tipo contenedor", max_length=200, blank=True, null=True, default="No especificado")
    punto_limpio_estado_contenedor = models.CharField("Punto limpio estado", max_length=200, blank=True, null=True, default="No especificado")
    punto_limpio_senaletica = models.CharField("Punto limpio senalética", max_length=200, blank=True, null=True, default="No especificado")
    punto_limpio_observaciones = models.CharField("Punto limpio observaciones", max_length=500, blank=True, null=True)

    # Página 4
    puntos_limpios_por_pisos = models.CharField("Puntos limpios por pisos", max_length=200, blank=True, null=True, default="No hay")
    grillaPuntosLimpiosPisos = models.JSONField("Grilla puntos limpios por pisos", blank=True, null=True, default=dict)
    punto_limpio_edificio_observaciones = models.CharField("Punto limpio Edificio observaciones", max_length=500, blank=True, null=True)

    # Página 5
    acopioContenedores = models.CharField("Acopio contenedores", max_length=200, blank=True, null=True, default="No especificado")
    grilla = models.JSONField("Grilla", blank=True, null=True, default=dict)
    observaciones = models.CharField("Observaciones", max_length=500, blank=True, null=True)

    # Página 6
    acciones_tomadas = models.CharField("Acciones tomadas", max_length=500, blank=True, null=True)
    otras_observaciones = models.CharField("Otras observaciones", max_length=500, blank=True, null=True)

    # Página 7 (Escombro)
    escombro_limpio = models.CharField("Escombro limpio", max_length=200, choices=[('Aplica','Aplica'), ('No Aplica','No Aplica')], blank=True, null=True, default="No Aplica")
    escombro_checks = models.JSONField("Escombro checks", blank=True, null=True, default=list)
    escombro_otro_texto = models.CharField("Escombro otro texto", max_length=200, blank=True, null=True)
    escombro_observaciones = models.CharField("Escombro observaciones", max_length=500, blank=True, null=True)

    # Página 8 (Plástico)
    plastico = models.CharField("Plástico", max_length=200, choices=[('Aplica','Aplica'), ('No Aplica','No Aplica')], blank=True, null=True, default="No Aplica")
    plastico_opciones = models.JSONField("Plástico opciones", blank=True, null=True, default=list)
    plastico_otro = models.CharField("Plástico otro", max_length=200, blank=True, null=True)
    plastico_observaciones = models.CharField("Plástico observaciones", max_length=500, blank=True, null=True)

    # Página 9 (Papel y Cartón)
    papel_y_carton = models.CharField("Papel y cartón", max_length=200, choices=[('Aplica','Aplica'), ('No Aplica','No Aplica')], blank=True, null=True, default="No Aplica")
    papel_carton_opciones = models.JSONField("Papel cartón opciones", blank=True, null=True, default=list)
    papel_carton_otro = models.CharField("Papel cartón otro", max_length=200, blank=True, null=True)
    papel_carton_observaciones = models.CharField("Papel cartón observaciones", max_length=500, blank=True, null=True)

    # Página 10 (Metales)
    metales = models.CharField("Metales", max_length=200, choices=[('Aplica','Aplica'), ('No Aplica','No Aplica')], blank=True, null=True, default="No Aplica")
    metales_opciones = models.JSONField("Metales opciones", blank=True, null=True, default=list)
    metales_otro_texto = models.CharField("Metales otro texto", max_length=200, blank=True, null=True)
    metales_observaciones = models.CharField("Metales observaciones", max_length=500, blank=True, null=True)

    # Página 11 (Madera)
    madera = models.CharField("Madera", max_length=200, choices=[('Aplica','Aplica'), ('No Aplica','No Aplica')], blank=True, null=True, default="No Aplica")
    madera_opciones = models.JSONField("Madera opciones", blank=True, null=True, default=list)
    madera_otro = models.CharField("Madera otro", max_length=200, blank=True, null=True)
    madera_observaciones = models.CharField("Madera observaciones", max_length=500, blank=True, null=True)

    # Página 12 (Mezclados)
    mezclados = models.CharField("Mezclados", max_length=200, choices=[('Aplica','Aplica'), ('No Aplica','No Aplica')], blank=True, null=True, default="No Aplica")
    gridSelection = models.JSONField("Grid selection", blank=True, null=True, default=dict)
    mezclados_opciones = models.JSONField("Mezclados opciones", blank=True, null=True, default=list)
    mezclados_otro = models.CharField("Mezclados otro", max_length=200, blank=True, null=True)
    mezclados_observaciones = models.CharField("Mezclados observaciones", max_length=500, blank=True, null=True)

    # Página 13 (Punto Acopio)
    puntoAcopio = models.CharField("Punto Acopio", max_length=200, choices=[('Aplica','Aplica'), ('No Aplica','No Aplica')], blank=True, null=True, default="No Aplica")
    puntoAcopioGrid = models.JSONField("Punto Acopio Grid", blank=True, null=True, default=list)
    puntoAcopioOpciones = models.JSONField("Punto Acopio Opciones", blank=True, null=True, default=list)
    puntoAcopioOtro = models.CharField("Punto Acopio Otro", max_length=200, blank=True, null=True)
    puntoAcopioObservaciones = models.CharField("Punto Acopio Observaciones", max_length=500, blank=True, null=True)

    def __str__(self):
        return f"Formulario {self.id}"
