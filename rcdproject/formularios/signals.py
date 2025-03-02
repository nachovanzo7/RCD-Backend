from django.db.models.signals import post_save
from django.dispatch import receiver
import datetime
from formularios.models import Formularios
from materiales.models import Material
from visitas.models import Visita
from condiciondeobras.models import CondicionDeObra
from puntolimpio.models import PuntoLimpio, PuntoAcopio

@receiver(post_save, sender=Formularios)
def crear_visita(sender, instance, created, **kwargs):
    if created:
        motivo = instance.motivo_de_visita
        if instance.otro_motivo:
            motivo += " - " + instance.otro_motivo

        Visita.objects.create(
            obra=instance.obra,         
            tecnico=instance.tecnico,   
            fecha=datetime.date.today(),
            motivo=motivo,
            observaciones=instance.otras_observaciones,
            acciones_tomadas=instance.acciones_tomadas
        )

@receiver(post_save, sender=Formularios)
def crear_condicion_de_obra(sender, instance, created, **kwargs):
    if created:
        CondicionDeObra.objects.create(
            obra=instance.obra,
            jornal_ambiental=instance.participante_jornal_ambiental,
            operarios=instance.participante_operario,
            oficina_tecnica=instance.participante_oficina_tecnica,
            participantes_de_obra_observaciones=instance.participante_observaciones,
            limpieza_general_por_terreno=instance.limpieza_general_en_terreno,
            limpieza_general_por_pisos=instance.limpieza_general_en_pisos,
            limpieza_general_observaciones=instance.limpieza_general_observaciones,
            logistica_de_obra=instance.logistica_de_obra,
            logistica_de_obra_observaciones=instance.logistica_de_obra_observaciones,
        )

@receiver(post_save, sender=PuntoLimpio)
def crear_punto_limpio(sender, instance, created, **kwargs):
    if created and instance.PUNTOLIMPIO_CHOICES == 'si_hay':
        PuntoLimpio.objects.create(
            punto_limpio_ubicacion=instance.punto_limpio_ubicacion,
            punto_limpio_estructura=instance.punto_limpio_estructura,
            punto_limpio_tipo_contenedor=instance.punto_limpio_tio_contenedor,
            punto_limpio_estado_contenedor=instance.punto_limpio_estado_contenedor,
            punto_limpio_señaletica=instance.punto_limpio_señaletica,
            punto_limpio_observaciones_=instance.punto_limpio_observaciones,
            punto_limpio_por_pisos=instance.punto_limpio_por_pisos,
            punto_limpio_pisos=instance.punto_limpio_pisos,
            punto_limpio_ubicacion_pisos=instance.punto_limpio_ubicacion_pisos,
            punto_limpio_estructura_pisos=instance.punto_limpio_estructura_pisos,
            punto_limpio_tipo_contenedor_pisos=instance.punto_limpio_tipo_contenedor_pisos,
            punto_limpio_señaletica_pisos=instance.punto_limpio_señaletica_pisos,
            punto_limpio_observaciones_pisos=instance.punto_limpio_observaciones_pisos,
        )

@receiver(post_save, sender=PuntoAcopio)
def crear_punto_acopio(sender, instance, created, **kwargs):
    if created and instance.PUNTO_DE_ACOPIO == 'si_hay':
        acciones_tomadas=instance.acciones_tomadas,
        if instance.otras_observaciones:
            acciones_tomadas += '-' + instance.otras_observaciones
        PuntoAcopio.objects.create(
            punto_de_acopio_ubicacion=instance.punto_de_acopio_ubicacion,
            punto_de_acopio_estructura=instance.punto_de_acopio_estructura,
            punto_de_acopio_tipo_contenedor=instance.punto_de_acopio_tipo_contenedor,
            punto_de_acopio_estado_contenedor=instance.punto_de_acopio_estado_contenedor,
            punto_de_acopio_señaletica=instance.punto_de_acopio_señaletica,
            punto_de_acopio_observaciones=instance.punto_de_acopio_observaciones,
        )

@receiver(post_save, sender=Material)
def crear_material(sender, instance, created, **kwargs):
    if created:
        Material.objects.create(
            HAY_TIPO_MATERIAL_CHOICES=instance.HAY_TIPO_MATERIAL_CHOICES,
            escombro_limpio=instance.escombro_limpio,
            OBSERVACIONES_CHOICES_ESCOMBRO_LIMPIO=instance.OBSERVACIONES_CHOICES_ESCOMBRO_LIMPIO,
            escombro_limpio_observaciones=instance.escombro_limpio_observaciones,
            escombro_limpio_otras_observaciones=instance.escombro_limpio_otras_observaciones,
            plastico=instance.plastico,
            OBSERVACIONES_CHOICES_PLASTICO=instance.OBSERVACIONES_CHOICES_PLASTICO,
            plastico_observaciones=instance.plastico_observaciones,
            plastico_otras_observaciones=instance.plastico_otras_observaciones,
            papel_y_carton=instance.papel_y_carton,
            OBSERVACIONES_CHOICES_PAPEL_Y_CARTON=instance.OBSERVACIONES_CHOICES_PAPEL_Y_CARTON,
            papel_y_carton_observaciones=instance.papel_y_carton_observaciones,
            papel_y_carton_otras_observaciones=instance.papel_y_carton_otras_observaciones,
            metales=instance.metales,
            OBSERVACIONES_CHOICES_METALES=instance.OBSERVACIONES_CHOICES_METALES,
            metales_observaciones=instance.metales_observaciones,
            metales_otras_observaciones=instance.metales_otras_observaciones,
            madera=instance.madera,
            OBSERVACIONES_CHOICES_MADERA=instance.OBSERVACIONES_CHOICES_MADERA,
            madera_observaciones=instance.madera_observaciones,
            madera_otras_observaciones=instance.madera_otras_observaciones,
            mezclados=instance.mezclados,
            mezclados_separaciones=instance.mezclados_separaciones,
            OBSERVACIONES_CHOICES_MEZCLADOS=instance.OBSERVACIONES_CHOICES_MEZCLADOS,
            mezclados_observaciones=instance.mezclados_observaciones,
            mezclados_otras_observaciones=instance.mezclados_otras_observaciones,
            peligrosos=instance.peligrosos,
            OBSERVACIONES_CHOICES_PELIGROSOS=instance.OBSERVACIONES_CHOICES_PELIGROSOS,
            punto_de_acopio=instance.punto_de_acopio,
            peligrosos_observaciones=instance.peligrosos_observaciones,
            peligrosos_otras_observaciones=instance.peligrosos_otras_observaciones,
        )