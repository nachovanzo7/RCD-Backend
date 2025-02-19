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
    Permite al cliente registrar una obra, creando automáticamente la solicitud,
    y, opcionalmente, los puntos limpios y materiales asociados según los datos anidados.
    """
    def post(self, request):
        # Extraer la lista de puntos limpios del request (si se envía)
        puntos_data = request.data.pop("puntos_limpios", None)
        # Extraer la cantidad de puntos limpios si no se envían datos anidados
        cantidad_puntos = int(request.data.pop("cantidad_puntos_limpios", 1))
        # Extraer la lista de materiales del request (si se envía)
        materiales_data = request.data.pop("materiales", None)
        
        serializer_obra = ObraSerializer(data=request.data)
        if serializer_obra.is_valid():
            obra = serializer_obra.save()
            # Crear la solicitud de obra
            solicitud = SolicitudObra.objects.create(obra=obra)
            cliente = Cliente.objects.get(pk=obra.cliente.id)
            
            puntos_ids = []
            # Crear puntos limpios
            if puntos_data:
                for punto_data in puntos_data:
                    punto = PuntoLimpio.objects.create(obra=obra, **punto_data)
                    puntos_ids.append(punto.id)
            else:
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
            
            materiales_ids = []
            if materiales_data:
                for material_data in materiales_data:
                    try:
                        # Verificar si se envió el campo "punto_limpio"
                        if "punto_limpio" not in material_data:
                            punto_default = obra.puntos_limpios.first()
                            if not punto_default:
                                return Response(
                                    {'error': 'No se ha creado ningún punto limpio para asignar al material.'},
                                    status=status.HTTP_400_BAD_REQUEST
                                )
                            material_data["punto_limpio"] = punto_default
                        else:
                            # Si se envía, convertir el ID a instancia
                            punto_id = material_data["punto_limpio"]
                            try:
                                punto_inst = PuntoLimpio.objects.get(pk=punto_id)
                            except PuntoLimpio.DoesNotExist:
                                return Response(
                                    {'error': f'Punto limpio con id {punto_id} no existe.'},
                                    status=status.HTTP_400_BAD_REQUEST
                                )
                            material_data["punto_limpio"] = punto_inst
                        
                        # Convertir el ID del transportista a instancia
                        transportista_id = material_data.get("transportista")
                        if transportista_id:
                            try:
                                transportista_instancia = Transportista.objects.get(pk=transportista_id)
                            except Transportista.DoesNotExist:
                                return Response(
                                    {'error': f'Transportista con id {transportista_id} no existe.'},
                                    status=status.HTTP_400_BAD_REQUEST
                                )
                            material_data["transportista"] = transportista_instancia
                        
                        # Crear el material asociado a la obra
                        material = Material.objects.create(obra=obra, **material_data)
                        materiales_ids.append(material.id)
                    except ValidationError as e:
                        return Response(e.message_dict, status=status.HTTP_400_BAD_REQUEST)
            
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
    # falta retornar el id del cliente que genera la solicitud

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
        
        # Actualizar estado a "rechazado"
        solicitud.estado = 'rechazado'
        solicitud.save()
        
        # Obtener la obra asociada
        obra = solicitud.obra
        # Eliminar los puntos limpios asociados a la obra
        obra.puntos_limpios.all().delete()
        # Eliminar los materiales asociados a la obra
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
    