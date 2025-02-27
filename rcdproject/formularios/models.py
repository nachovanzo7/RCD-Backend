from django.db import models
from tecnicos.models import Tecnico
from obras.models import Obra

class Formularios(models.Model):
    id = models.AutoField(primary_key=True)
    tecnico = models.ForeignKey(Tecnico, on_delete=models.CASCADE, related_name='formularios') 
    obra = models.ForeignKey(Obra, on_delete=models.CASCADE, related_name='formularios')
    fecha = models.DateField("Fecha")
    motivo_de_visita = models.CharField("Motivo de visita", max_length=200) 
    otro_motivo = models.CharField("Otro motivo", max_length=200, blank=True, null=True)
    participante_jornal_ambiental = models.CharField("Participante jornal ambiental", max_length=200)
    participante_operario = models.CharField("Participante jornal ambiental", max_length=200) 
    participante_oficina_tecnica = models.CharField("Participante jornal ambiental", max_length=200) 
    participante_observaciones = models.CharField("Participante jornal ambiental", max_length=500)
    limpieza_general_en_terreno = models.CharField("Limpieza general en terreno", max_length=200)
    limpieza_general_en_pisos = models.CharField("Limpieza general en terreno", max_length=200)
    limpieza_general_observaciones = models.CharField("Limpieza general en terreno", max_length=500)
    logistica_de_obra = models.CharField("Logística de obra", max_length=200) #
    logistica_de_obra_observaciones = models.CharField("Logística de obra", max_length=500)
    PUNTOLIMPIO_CHOICES = [
        ('si_hay', 'Sí Hay'),
        ('no_hay', 'No Hay'),
    ]
    punto_limpio = models.CharField("Punto limpio", max_length=200, choices=PUNTOLIMPIO_CHOICES)
    punto_limpio_ubicacion = models.CharField("Punto limpio ubicación", max_length=200)
    punto_limpio_estructura = models.CharField("Punto limpio ubicación", max_length=200)
    punto_limpio_tipo_contenedor = models.CharField("Punto limpio ubicación", max_length=200)
    punto_limpio_estado_contenedor = models.CharField("Punto limpio ubicación", max_length=200)
    punto_limpio_señaletica = models.CharField("Punto limpio ubicación", max_length=200)
    punto_limpio_observaciones = models.CharField("Punto limpio ubicación", max_length=500)
    PUNTOLIMPIOUBICACIONPORPISOS_CHOICES = [
        ('si_hay', 'Sí Hay'),
        ('no_hay', 'No Hay'),
    ]
    puntos_limpios_por_pisos = models.CharField("Puntos limpios por pisos", max_length=200, choices=PUNTOLIMPIOUBICACIONPORPISOS_CHOICES)
    punto_limpio_pisos = models.CharField("Punto limpio", max_length=200, choices=PUNTOLIMPIO_CHOICES)
    punto_limpio_ubicacion_pisos = models.CharField("Punto limpio ubicación", max_length=200)
    punto_limpio_estructura_pisos = models.CharField("Punto limpio ubicación", max_length=200)
    punto_limpio_tipo_contenedor_pisos = models.CharField("Punto limpio ubicación", max_length=200)
    punto_limpio_estado_contenedor_pisos = models.CharField("Punto limpio ubicación", max_length=200)
    punto_limpio_señaletica_pisos = models.CharField("Punto limpio ubicación", max_length=200)
    punto_limpio_observaciones_pisos = models.CharField("Punto limpio ubicación", max_length=500)
    PUNTO_DE_ACOPIO = [
        ('si_hay', 'Sí Hay'),
        ('no_hay', 'No Hay'),
    ]
    punto_de_acopio_ubicacion = models.CharField("Punto de acopio", max_length=200, choices=PUNTO_DE_ACOPIO)
    punto_de_acopio_estructura = models.CharField("Punto de acopio", max_length=200, choices=PUNTO_DE_ACOPIO)
    punto_de_acopio_tipo_contenedor = models.CharField("Punto de acopio", max_length=200, choices=PUNTO_DE_ACOPIO)
    punto_de_acopio_estado_contenedor = models.CharField("Punto de acopio", max_length=200, choices=PUNTO_DE_ACOPIO)
    punto_de_acopio_señaletica = models.CharField("Punto de acopio", max_length=200, choices=PUNTO_DE_ACOPIO)
    punto_de_acopio_observaciones = models.CharField("Punto de acopio", max_length=500, choices=PUNTO_DE_ACOPIO)
    acciones_tomadas = models.CharField("Acciones tomadas", max_length=500)
    otras_observaciones = models.CharField("Otras observaciones", max_length=500)
    HAY_TIPO_MATERIAL_CHOICES = [
        ('aplica', 'Aplica'),
        ('no_aplica', 'No Aplica'),
    ]
    escombro_limpio = models.CharField("Escombro limpio", max_length=200, choices=HAY_TIPO_MATERIAL_CHOICES)
    OBSERVACIONES_CHOICES_ESCOMBRO_LIMPIO = [
        ('acopio_a_granel', 'Acopio a granel'),
        ('en_volquetas', 'En volquetas'),
        ('en_bolson_azul', 'En bolson azul'),
        ('poco_accesible', 'Poco accesible'),
        ('vacio', 'Vacio'),
        ('lleno', 'Lleno'),
        ('se_esta_reutilizando_en_obra', 'Se está reutilizando en obra'),
        ('contiene_resiuduos_que_no_corresponden', 'Contiene residuos que no corresponden'),
        ('otro', 'Otro'),
    ]
    escombro_limpio_observaciones = models.CharField("Escombro limpio", max_length=500, choices=OBSERVACIONES_CHOICES_ESCOMBRO_LIMPIO)
    escombro_limpio_otras_observaciones = models.CharField("Escombro limpio", max_length=500)
    plastico = models.CharField("Plástico", max_length=200, choices=HAY_TIPO_MATERIAL_CHOICES)
    OBSERVACIONES_CHOICES_PLASTICO = [
        ('vacio', 'Vacio'),
        ('lleno', 'Lleno'),
        ('contiene_plasticos_no_reciclables', 'Contiene plásticos no reciclables'),
        ('contiene_residuos_que_no_corresponden', 'Contiene residuos que no corresponden'),
        ('sucio_y/o_contaminado', 'Sucio y/o contaminado'),
        ('poca_compactacion', 'Poca compactación'),
        ('poco_accesible', 'Poco accesible'),
        ('no_esta_implementada_la_fraccion', 'No está implementada la fracción'),
        ('otro', 'Otro'),
    ]
    plastico_observaciones = models.CharField("Plástico", max_length=500, choices=OBSERVACIONES_CHOICES_PLASTICO)
    plastico_otras_observaciones = models.CharField("Plástico", max_length=500)
    papel_y_carton = models.CharField("Papel y cartón", max_length=200, choices=HAY_TIPO_MATERIAL_CHOICES)
    OBSERVACIONES_CHOICES_PAPEL_Y_CARTON = [
        ('vacio', 'Vacio'),
        ('lleno', 'Lleno'),
        ('falta_proteccion_interperie', 'Falta protección interperie'),
        ('contiene_residuos_que_no_corresponden', 'Contiene residuos que no corresponden'),
        ('sucio_y/o_contaminado', 'Sucio y/o contaminado'),
        ('poca_compactacion', 'Poca compactación'),
        ('poco_accesible', 'Poco accesible'),
        ('no_esta_implementada_la_fraccion', 'No está implementada la fracción'),
        ('otro', 'Otro'),
    ]
    papel_y_carton_observaciones = models.CharField("Papel y cartón", max_length=500, choices=OBSERVACIONES_CHOICES_PAPEL_Y_CARTON)
    papel_y_carton_otras_observaciones = models.CharField("Papel y cartón", max_length=500)
    metales = models.CharField("Metales", max_length=200, choices=HAY_TIPO_MATERIAL_CHOICES)
    OBSERVACIONES_CHOICES_METALES = [
        ('a_granel', 'A granel'),
        ('en_cajon_prefabricado', 'En cajón prefabricado'),
        ('se_utiliza_en_obra', 'Se utiliza en obra'),
        ('mucha_cantidad', 'Mucha cantidad'),
        ('poco_accesible', 'Poco accesible'),
        ('otro', 'Otro'),
    ]
    metales_observaciones = models.CharField("Metales", max_length=500, choices=OBSERVACIONES_CHOICES_METALES)
    metales_otras_observaciones = models.CharField("Metales", max_length=500)
    madera = models.CharField("Madera", max_length=200, choices=HAY_TIPO_MATERIAL_CHOICES)
    OBSERVACIONES_CHOICES_MADERA = [
        ('a_granel', 'A granel'),
        ('mala_organizacion', 'Mala organización'),
        ('mucha_cantidad', 'Mucha cantidad'),
        ('se_esta_reutilizando_en_obra', 'Se está reutilizando en obra'),
        ('contaminado_con_aceite_pintura_pegamento', 'Contaminado con aceite, pintura, pegamento'),
        ('otro', 'Otro'),
    ]
    madera_observaciones = models.CharField("Madera", max_length=500, choices=OBSERVACIONES_CHOICES_MADERA)
    madera_otras_observaciones = models.CharField("Madera", max_length=500)
    mezclados = models.CharField("Mezclados", max_length=200, choices=HAY_TIPO_MATERIAL_CHOICES)
    mezclados_separaciones = models.CharField("Mezclados", max_length=200)
    OBSERVACIONES_CHOICES_MEZCLADOS = [
        ('presencia_de_materiales_valorizables', 'Presencia de materiales valorizables'),
        ('mucha_cantidad', 'Mucha cantidad'),
        ('se_hizo_retiro', 'Se hizo retiro'),
        ('contiene_residuos_peligrosos', 'Contiene residuos peligrosos'),
        ('otros', 'Otros'),
    ]
    mezclados_observaciones = models.CharField("Mezclados", max_length=500, choices=OBSERVACIONES_CHOICES_MEZCLADOS)
    mezclados_otras_observaciones = models.CharField("Mezclados", max_length=500)
    peligrosos = models.CharField("Peligrosos", max_length=200, choices=HAY_TIPO_MATERIAL_CHOICES)
    OBSERVACIONES_CHOICES_PELIGROSOS = [
        ('tanques_vacios', 'Tanques vacíos'),
        ('tanques_llenos', 'Tanques llenos'),
        ('falta_cajon_antiderrame', 'Falta cajón antiderrame'),
        ('falta_orden', 'Falta orden'),
        ('contiene_residuos_que_no_corresponden', 'Contiene residuos que no corresponden'),
        ('otro', 'Otro'),
    ]
    punto_de_acopio = models.CharField("Punto de acopio", max_length=200)
    peligrosos_observaciones = models.CharField("Peligrosos", max_length=500, choices=OBSERVACIONES_CHOICES_PELIGROSOS)
    peligrosos_otras_observaciones = models.CharField("Peligrosos", max_length=500)

    


# Agregar datos a las diferentes tablas