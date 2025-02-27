from django.db.models.signals import post_save
from django.dispatch import receiver
import datetime
from formularios.models import Formularios
from visitas.models import Visita
from condiciondeobras.models import CondicionDeObra

@receiver(post_save, sender=Formularios)
def crear_visita(sender, instance, created, **kwargs):
    if created:
        # Combinar 'motivo_de_visita' y 'otro_motivo'
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

