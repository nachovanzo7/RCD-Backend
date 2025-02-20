from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from django.core.exceptions import ValidationError
from .models import Obra, SolicitudObra
from .serializers import ObraSerializer, SolicitudObraSerializer, SolicitudObraAdminSerializer
from clientes.models import Cliente
from puntolimpio.models import PuntoLimpio
from materiales.models import Material
from transportistas.models import Transportista

class RegistroObra(APIView):
    """
    Permite registrar una obra, creando la solicitud y, opcionalmente, los puntos limpios y materiales asociados.
    Se espera que en cada punto limpio anidado se incluya un array "materiales" con los tipos de material (ej. "madera").
    """
    def post(self, request):
        puntos_data = request.data.pop("puntos_limpios", None)
        cantidad_puntos = int(request.data.pop("cantidad_puntos_limpios", 1))
        serializer_obra = ObraSerializer(data=request.data)
        if serializer_obra.is_valid():
            obra = serializer_obra.save()
            solicitud = SolicitudObra.objects.create(obra=obra)
            cliente = Cliente.objects.get(pk=obra.cliente.id)
            
            puntos_ids = []
            materiales_ids = []
            if puntos_data:
                for punto_data in puntos_data:
                    # Extraemos la lista de materiales para este punto
                    materiales_list = punto_data.pop("materiales", [])
                    # Si se envía "ventilacion" en los datos del punto, se elimina,
                    # ya que ese campo no pertenece al modelo PuntoLimpio.
                    punto_data.pop("ventilacion", None)
                    
                    # Creamos el PuntoLimpio sin el campo 'ventilacion'
                    punto = PuntoLimpio.objects.create(obra=obra, **punto_data)
                    puntos_ids.append(punto.id)
                    
                    for tipo_material in materiales_list:
                        default_transportista = Transportista.objects.filter(tipo_material=tipo_material).first()
                        if not default_transportista:
                            return Response(
                                {"error": f"Es necesario dar de alta un transportista para el material: '{tipo_material}'."},
                                status=status.HTTP_400_BAD_REQUEST
                            )
                        try:
                            # Si el material es 'peligrosos', asignamos ventilacion = "Necesario"
                            ventilacion_valor = "Necesario" if tipo_material == "peligrosos" else ""
                            material = Material.objects.create(
                                obra=obra,
                                punto_limpio=punto,
                                transportista=default_transportista,
                                descripcion="No especificado",
                                proteccion="No especificado",
                                tipo_contenedor=punto.tipo_contenedor,
                                estado_del_contenedor="No especificado",
                                esta_lleno=False,
                                tipo_material=tipo_material,
                                ventilacion=ventilacion_valor
                            )
                            materiales_ids.append({'id': material.id, 'tipo_material': material.tipo_material})
                        except ValidationError as e:
                            return Response(e.message_dict, status=status.HTTP_400_BAD_REQUEST)
            else:
                # Si no se envían puntos limpios, se crea uno por defecto
                for _ in range(cantidad_puntos):
                    punto = PuntoLimpio.objects.create(
                        obra=obra,
                        ubicacion="No especificado",
                        accesibilidad="en_planta_baja",
                        metros_cuadrados=0,
                        estructura="No especificado",
                        tipo_contenedor="No especificado",
                        puntaje=0,
                        señaletica=True,
                        observaciones="",
                        clasificacion="no_aplica"
                    )
                    puntos_ids.append(punto.id)
            
            return Response({
                'mensaje': 'Obra registrada, pendiente de aprobación.',
                'obra': ObraSerializer(obra, context={'request': request}).data,
                'solicitud': SolicitudObraSerializer(solicitud, context={'request': request}).data,
                'ID de cliente': cliente.id,
                'puntos_limpios_creados': puntos_ids,
                'materiales_creados': materiales_ids
            }, status=status.HTTP_201_CREATED)
        return Response(serializer_obra.errors, status=status.HTTP_400_BAD_REQUEST)


class ListarSolicitudesObra(APIView):
    """
    Lista todas las solicitudes de obras para el administrador
    """
    def get(self, request):
        solicitudes = SolicitudObra.objects.all()
        serializer = SolicitudObraAdminSerializer(solicitudes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class AprobarSolicitudObra(APIView):
    """
    Permite al administrador aceptar una solicitud de obra
    """
    def put(self, request, pk):
        try:
            solicitud = SolicitudObra.objects.get(pk=pk)
        except SolicitudObra.DoesNotExist:
            return Response({'error': 'Su solicitud no fue encontrada.'}, status=status.HTTP_404_NOT_FOUND)
        
        if solicitud.estado != 'pendiente':
            return Response({'error': 'La solicitud ya ha sido procesada.'}, status=status.HTTP_400_BAD_REQUEST)
        
        solicitud.estado = 'Aceptado'
        solicitud.fecha_solicitud = timezone.now()
        solicitud.save()
        return Response({'mensaje': 'Su solicitud de obra fue aprobada.'}, status=status.HTTP_200_OK)

class RechazarSolicitudObra(APIView):
    """
    Permite al administrador rechazar una solicitud de obra.
    Al rechazar, se eliminan los puntos limpios y los materiales asociados a la obra.
    """
    def put(self, request, pk):
        try:
            solicitud = SolicitudObra.objects.get(pk=pk)
        except SolicitudObra.DoesNotExist:
            return Response({'error': 'Su solicitud no fue encontrada.'}, status=status.HTTP_404_NOT_FOUND)
        
        if solicitud.estado != 'pendiente':
            return Response({'error': 'La solicitud ya ha sido procesada.'}, status=status.HTTP_400_BAD_REQUEST)
        
        solicitud.estado = 'rechazado'
        solicitud.save()
        
        obra = solicitud.obra
        obra.puntos_limpios.all().delete()
        obra.materiales.all().delete()
        
        return Response(
            {'mensaje': 'Su solicitud de obra fue rechazada y se eliminaron los puntos limpios y materiales asociados.'},
            status=status.HTTP_200_OK
        )

class ListarObrasAprobadas(APIView):
    """
    Muestra una lista con las obras que fueron aprobadas
    """
    def get(self, request):
        obras = Obra.objects.filter(solicitud__estado='Aceptado')
        serializer = ObraSerializer(obras, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ModificarDatosObra(APIView):
    """
    Modificar datos de obras
    """
    def patch(self, request, pk):
        try:
            obra = Obra.objects.get(pk=pk)
        except Obra.DoesNotExist:
            return Response({'error': 'Obra no encontrada.'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ObraSerializer(obra, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EliminarObra(APIView):
    """
    Eliminar una obra
    """
    def delete(self, request, pk):
        try:
            obra = Obra.objects.get(pk=pk)
        except Obra.DoesNotExist:
            return Response({'error': 'Obra no encontrada.'}, status=status.HTTP_404_NOT_FOUND)
        
        obra.delete()
        return Response({'mensaje': 'Obra eliminada.'}, status=status.HTTP_200_OK)
    