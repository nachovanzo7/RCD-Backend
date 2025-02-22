from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from .models import CoordinacionRetiro
from .serializers import CoordinacionRetiroSerializer


class CrearCoordinacionRetiro(APIView):
    """
    Registra una nueva solicitud de coordinación de retiro con estado 'pendiente'.
    Se valida que el transportista pueda transportar el tipo de material solicitado.
    """
    def post(self, request):
        serializer = CoordinacionRetiroSerializer(data=request.data)
        if serializer.is_valid():
            transportista = serializer.validated_data.get("transportista")
            tipo_material = serializer.validated_data.get("tipo_material")
            estado = serializer.validated_data.get("estado")
            if transportista.estado != 'activo':
                return Response(
                    {"error": "El transportista seleccionado no está activo."}, status=status.HTTP_400_BAD_REQUEST)
            if transportista.tipo_material != tipo_material:
                return Response(
                    {"error": "El transportista seleccionado no puede transportar este tipo de material."}, status=status.HTTP_400_BAD_REQUEST)
            coordinacion = serializer.save()
            return Response(CoordinacionRetiroSerializer(coordinacion, context={'request': request}).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ListarCoordinacionesRetiro(APIView):
    """
    Lista todas las coordinaciones de retiro.
    """
    def get(self, request):
        coordinaciones = CoordinacionRetiro.objects.all()
        serializer = CoordinacionRetiroSerializer(coordinaciones, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class AceptarCoordinacionRetiro(APIView):
    """
    Permite al administrador aceptar una solicitud de coordinación de retiro.
    Al aceptar, se actualiza el estado a 'aceptado' (y se puede asignar la fecha de retiro).
    """
    def put(self, request, pk):
        try:
            coordinacion = CoordinacionRetiro.objects.get(pk=pk)
        except CoordinacionRetiro.DoesNotExist:
            return Response({'error': 'Solicitud no encontrada.'}, status=status.HTTP_404_NOT_FOUND)
        
        if coordinacion.estado != 'pendiente':
            return Response({'error': 'La solicitud ya ha sido procesada.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Actualizamos el estado a 'aceptado'
        coordinacion.estado = 'aceptado'
        # Opcional: asignar fecha de retiro automáticamente si no se envía
        if 'fecha_retiro' not in request.data:
            coordinacion.fecha_retiro = timezone.now()
        else:
            coordinacion.fecha_retiro = request.data['fecha_retiro']
        coordinacion.save()
        return Response({'mensaje': 'Solicitud de coordinación de retiro aceptada.'},status=status.HTTP_200_OK)

class RechazarCoordinacionRetiro(APIView):
    """
    Permite al administrador rechazar una solicitud de coordinación de retiro.
    """
    def put(self, request, pk):
        try:
            coordinacion = CoordinacionRetiro.objects.get(pk=pk)
        except CoordinacionRetiro.DoesNotExist:
            return Response({'error': 'Solicitud no encontrada.'}, status=status.HTTP_404_NOT_FOUND)
        
        if coordinacion.estado != 'pendiente':
            return Response({'error': 'La solicitud ya ha sido procesada.'}, status=status.HTTP_400_BAD_REQUEST)
        
        coordinacion.estado = 'rechazado'
        coordinacion.save()
        return Response({'mensaje': 'Solicitud de coordinación de retiro rechazada.'},
                        status=status.HTTP_200_OK)

class ListarSolicitudesAceptadasCoordinacion(APIView):
    """
    Lista todas las solicitudes de coordinación de retiro aceptadas.
    """
    def get(self, request):
        solicitudes = CoordinacionRetiro.objects.filter(estado='aceptado')
        serializer = CoordinacionRetiroSerializer(solicitudes, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

