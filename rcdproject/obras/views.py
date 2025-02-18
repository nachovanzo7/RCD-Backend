from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Obra, SolicitudObra
from .serializers import ObraSerializer, SolicitudObraSerializer, SolicitudObraAdminSerializer
from clientes.models import Cliente
from puntolimpio.models import PuntoLimpio

class RegistroObra(APIView):
    """
    Permite al cliente registrar una obra, creando automáticamente la solicitud
    y los puntos limpios asociados según la cantidad indicada.
    """
    def post(self, request):
        # Extraer la cantidad de puntos limpios del request; si no se envía, por defecto se crea 1
        cantidad_puntos = int(request.data.pop("cantidad_puntos_limpios", 1))
        
        serializer_obra = ObraSerializer(data=request.data)
        if serializer_obra.is_valid():
            obra = serializer_obra.save()
            solicitud = SolicitudObra.objects.create(obra=obra)
            cliente = Cliente.objects.get(pk=obra.cliente.id)
            
            # Crear la cantidad indicada de puntos limpios
            puntos_ids = []
            for _ in range(cantidad_puntos):
                punto = PuntoLimpio.objects.create(
                    obra=obra,
                    ubicacion="No especificado",
                    accesibilidad="en_planta_baja",
                    cantidad=0,
                    metros_cuadrados=0,
                    estructura="No especificado",
                    tipo_contenedor="No especificado",
                    puntaje=0,
                    señaletica=True,
                    observaciones="",
                    clasificacion="no_aplica"  # Asegúrate de que 'no_aplica' esté entre los choices
                )
                puntos_ids.append(punto.id)
            
            return Response({'mensaje': 'Obra registrada, pendiente de aprobación.','obra': ObraSerializer(obra, context={'request': request}).data,'solicitud': SolicitudObraSerializer(solicitud, context={'request': request}).data,'ID de cliente': cliente.id,'puntos_limpios_creados': puntos_ids}, status=status.HTTP_201_CREATED)
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
        solicitud.save()
        return Response({'mensaje': 'Su solicitud de obra fue aprobada.'}, status=status.HTTP_200_OK)

class RechazarSolicitudObra(APIView):
    """
    Permite al administrador rechazar una solicitud de obra
    """
    def put(self, request, pk):
        try:
            solicitud = SolicitudObra.objects.get(pk=pk)
        except SolicitudObra.DoesNotExist:
            return Response({'error': 'Su solicitud no fue encontrada.'}, status=status.HTTP_404_NOT_FOUND)
        
        if solicitud.estado != 'pendiente':
            return Response({'error': 'La solicitud ya ha sido procesada.'}, status=status.HTTP_400_BAD_REQUEST)
        
        solicitud.estado = 'Rechazado'
        solicitud.save()
        return Response({'mensaje': 'Su solicitud de obra fue rechazada.'}, status=status.HTTP_200_OK)

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
    