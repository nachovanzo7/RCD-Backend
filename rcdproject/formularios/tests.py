# formularios/tests.py
import datetime
from django.test import TestCase
from django.db.models.signals import post_save
from clientes.models import Cliente
from obras.models import Obra
from tecnicos.models import Tecnico
from formularios.models import Formularios
from visitas.models import Visita
from condiciondeobras.models import CondicionDeObra

# Importa la señal que causa el error
from usuarios.signals import crear_usuario_asociado

class SignalTestCase(TestCase):
    def setUp(self):
        # Desconecta la señal que crea un usuario asociado al crear un Cliente
        post_save.disconnect(crear_usuario_asociado, sender=Cliente)

        # Ahora crea la instancia de Cliente sin que se dispare la señal problemática.
        self.cliente = Cliente.objects.create(
            nombre="Cliente Test",
            fecha_ingreso=datetime.date.today()
        )
        # Crea la instancia de Obra asociándola al Cliente
        self.obra = Obra.objects.create(nombre_obra="Obra Test", cliente=self.cliente)
        # Crea una instancia de Técnico (ajusta los campos requeridos según tu modelo)
        self.tecnico = Tecnico.objects.create(nombre="Técnico Test")

    def test_signal_crea_visita_y_condicion_de_obra(self):
        # Crea una instancia de Formularios con todos los datos requeridos
        form = Formularios.objects.create(
            obra=self.obra,
            tecnico=self.tecnico,
            fecha=datetime.date.today(),
            motivo_de_visita="Inspección",
            otro_motivo="Mantenimiento",
            participante_jornal_ambiental="Juan Pérez",
            participante_operario="Ana López",
            participante_oficina_tecnica="Carlos García",
            participante_observaciones="Observaciones de prueba",
            limpieza_general_en_terreno="Buen estado",
            limpieza_general_en_pisos="Piso limpio",
            limpieza_general_observaciones="Sin detalles",
            logistica_de_obra="Coordinado",
            logistica_de_obra_observaciones="Sin inconvenientes",
            punto_limpio="si_hay",
            punto_limpio_ubicacion="Ubicación 1",
            punto_limpio_estructura="Estructura 1",
            punto_limpio_tipo_contenedor="Tipo 1",
            punto_limpio_estado_contenedor="Estado 1",
            punto_limpio_señaletica="Señalética 1",
            punto_limpio_observaciones="Observaciones 1",
            puntos_limpios_por_pisos="si_hay",
            punto_limpio_pisos="si_hay",
            punto_limpio_ubicacion_pisos="Ubicación pisos",
            punto_limpio_estructura_pisos="Estructura pisos",
            punto_limpio_tipo_contenedor_pisos="Tipo pisos",
            punto_limpio_estado_contenedor_pisos="Estado pisos",
            punto_limpio_señaletica_pisos="Señalética pisos",
            punto_limpio_observaciones_pisos="Observaciones pisos",
            punto_de_acopio_ubicacion="si_hay",
            punto_de_acopio_estructura="si_hay",
            punto_de_acopio_tipo_contenedor="si_hay",
            punto_de_acopio_estado_contenedor="si_hay",
            punto_de_acopio_señaletica="si_hay",
            punto_de_acopio_observaciones="si_hay",
            acciones_tomadas="Se ajustaron equipos",
            otras_observaciones="Todo en orden",
            escombro_limpio="aplica",
            escombro_limpio_observaciones="acopio_a_granel",
            escombro_limpio_otras_observaciones="Otros",
            plastico="aplica",
            plastico_observaciones="vacio",
            plastico_otras_observaciones="Otros",
            papel_y_carton="aplica",
            papel_y_carton_observaciones="vacio",
            papel_y_carton_otras_observaciones="Otros",
            metales="aplica",
            metales_observaciones="a_granel",
            metales_otras_observaciones="Otros",
            madera="aplica",
            madera_observaciones="a_granel",
            madera_otras_observaciones="Otros",
            mezclados="aplica",
            mezclados_separaciones="Separado",
            mezclados_observaciones="presencia_de_materiales_valorizables",
            mezclados_otras_observaciones="Otros",
            peligrosos="aplica",
            punto_de_acopio="Punto de acopio",
            peligrosos_observaciones="tanques_vacios",
            peligrosos_otras_observaciones="Otros"
        )

        # Verifica que se haya creado una entrada en Visita
        visita = Visita.objects.get(obra=self.obra, tecnico=self.tecnico)
        self.assertEqual(visita.motivo, "Inspección - Mantenimiento")
        self.assertEqual(visita.observaciones, "Todo en orden")
        self.assertEqual(visita.acciones_tomadas, "Se ajustaron equipos")

        # Verifica que se haya creado una entrada en CondicionDeObra
        condicion = CondicionDeObra.objects.get(obra=self.obra)
        self.assertEqual(condicion.jornal_ambiental, "Juan Pérez")
        self.assertEqual(condicion.operarios, "Ana López")
        self.assertEqual(condicion.oficina_tecnica, "Carlos García")
        self.assertEqual(condicion.participantes_de_obra_observaciones, "Observaciones de prueba")
        self.assertEqual(condicion.limpieza_general_por_terreno, "Buen estado")
        self.assertEqual(condicion.limpieza_general_por_pisos, "Piso limpio")
        self.assertEqual(condicion.limpieza_general_observaciones, "Sin detalles")
        self.assertEqual(condicion.logistica_de_obra, "Coordinado")
        self.assertEqual(condicion.logistica_de_obra_observaciones, "Sin inconvenientes")
