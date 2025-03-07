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
        # Si no hay técnico asignado, no se crea la visita y se registra un mensaje de advertencia.
        if not instance.tecnico:
            print("No se crea la visita porque el formulario no tiene técnico asignado.")
            return

        motivo = instance.motivo_de_visita or ""
        if instance.otro_motivo:
            motivo += " - " + instance.otro_motivo

        Visita.objects.create(
            obra=instance.obra,         
            tecnico=instance.tecnico,   # Aquí se usa el técnico del formulario
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

@receiver(post_save, sender=Formularios)
def actualizar_punto_limpio(sender, instance, created, **kwargs):
    if instance.punto_limpio == 'si_hay':
        try:
            punto_limpio = PuntoLimpio.objects.get(obra=instance.obra)
        except PuntoLimpio.DoesNotExist:
            return

        punto_limpio.punto_limpio_ubicacion = instance.punto_limpio_ubicacion
        punto_limpio.punto_limpio_estructura = instance.punto_limpio_estructura
        punto_limpio.punto_limpio_tipo_contenedor = instance.punto_limpio_tipo_contenedor
        punto_limpio.punto_limpio_estado_contenedor = instance.punto_limpio_estado_contenedor
        punto_limpio.punto_limpio_señaletica = instance.punto_limpio_señaletica
        punto_limpio.punto_limpio_observaciones = instance.punto_limpio_observaciones
        punto_limpio.punto_limpio_por_pisos = instance.punto_limpio_por_pisos
        punto_limpio.punto_limpio_pisos = instance.punto_limpio_pisos
        punto_limpio.punto_limpio_ubicacion_pisos = instance.punto_limpio_ubicacion_pisos
        punto_limpio.punto_limpio_estructura_pisos = instance.punto_limpio_estructura_pisos
        punto_limpio.punto_limpio_tipo_contenedor_pisos = instance.punto_limpio_tipo_contenedor_pisos
        punto_limpio.punto_limpio_señaletica_pisos = instance.punto_limpio_señaletica_pisos
        punto_limpio.punto_limpio_observaciones_pisos = instance.punto_limpio_observaciones_pisos

        punto_limpio.save()

@receiver(post_save, sender=Formularios)
def actualizar_punto_acopio(sender, instance, created, **kwargs):
    if getattr(instance, 'punto_acopio', None) == 'si_hay':
        try:
            punto_acopio = PuntoAcopio.objects.get(obra=instance.obra)
        except PuntoAcopio.DoesNotExist:
            return

        punto_acopio.ubicacion = getattr(instance, 'punto_de_acopio_ubicacion', punto_acopio.ubicacion)
        punto_acopio.estructura = getattr(instance, 'punto_de_acopio_estructura', punto_acopio.estructura)
        punto_acopio.tipo_contenedor = getattr(instance, 'punto_de_acopio_tipo_contenedor', punto_acopio.tipo_contenedor)
        punto_acopio.observaciones = getattr(instance, 'punto_de_acopio_observaciones', punto_acopio.observaciones)

        punto_acopio.save()
