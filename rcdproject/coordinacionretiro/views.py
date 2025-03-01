from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from .models import CoordinacionRetiro
from .serializers import CoordinacionRetiroSerializer
from usuarios.permisos import RutaProtegida

class CrearCoordinacionRetiro(APIView):
    """
    Registra una nueva solicitud de coordinación de retiro con estado 'pendiente'.
    Se valida que el transportista pueda transportar el tipo de material solicitado.
    """
    permission_classes = [RutaProtegida(['superadmin', 'coordinadorlogistico', 'cliente'])]
    
    def post(self, request):
        serializer = CoordinacionRetiroSerializer(data=request.data)
        if serializer.is_valid():
            transportista = serializer.validated_data.get("transportista")
            tipo_material = serializer.validated_data.get("tipo_material")
            estado = serializer.validated_data.get("estado")
            if transportista.estado != 'activo':
                return Response(
                    {"error": "El transportista seleccionado no está activo."}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            if transportista.tipo_material != tipo_material:
                return Response(
                    {"error": "El transportista seleccionado no puede transportar este tipo de material."}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            coordinacion = serializer.save()
            return Response(
                CoordinacionRetiroSerializer(coordinacion, context={'request': request}).data, 
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListarCoordinacionesRetiro(APIView):
    """
    Lista todas las coordinaciones de retiro pendientes.
    """
    permission_classes = [RutaProtegida(['superadmin', 'coordinadorlogistico', 'cliente'])]
    
    def get(self, request):
        coordinaciones = CoordinacionRetiro.objects.filter(estado='pendiente')
        serializer = CoordinacionRetiroSerializer(coordinaciones, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class AceptarCoordinacionRetiro(APIView):
    """
    Permite al administrador aceptar una solicitud de coordinación de retiro.
    Al aceptar, se actualiza el estado a 'aceptado' y se asigna la fecha de retiro.
    """
    permission_classes = [RutaProtegida(['superadmin', 'coordinadorlogistico'])]
    
    def put(self, request, pk):
        try:
            coordinacion = CoordinacionRetiro.objects.get(pk=pk)
        except CoordinacionRetiro.DoesNotExist:
            return Response({'error': 'Solicitud no encontrada.'}, status=status.HTTP_404_NOT_FOUND)
        
        if coordinacion.estado != 'pendiente':
            return Response({'error': 'La solicitud ya ha sido procesada.'}, status=status.HTTP_400_BAD_REQUEST)
        
        coordinacion.estado = 'aceptado'
        # Asignar fecha de retiro: si no se envía en request.data, se asigna la fecha actual
        if 'fecha_retiro' not in request.data:
            coordinacion.fecha_retiro = timezone.now()
        else:
            coordinacion.fecha_retiro = request.data['fecha_retiro']
        coordinacion.save()
        return Response({'mensaje': 'Solicitud de coordinación de retiro aceptada.'}, status=status.HTTP_200_OK)


class RechazarCoordinacionRetiro(APIView):
    """
    Permite al administrador rechazar una solicitud de coordinación de retiro.
    """
    permission_classes = [RutaProtegida(['superadmin', 'coordinadorlogistico'])]
    
    def put(self, request, pk):
        try:
            coordinacion = CoordinacionRetiro.objects.get(pk=pk)
        except CoordinacionRetiro.DoesNotExist:
            return Response({'error': 'Solicitud no encontrada.'}, status=status.HTTP_404_NOT_FOUND)
        
        if coordinacion.estado != 'pendiente':
            return Response({'error': 'La solicitud ya ha sido procesada.'}, status=status.HTTP_400_BAD_REQUEST)
        
        coordinacion.estado = 'rechazado'
        coordinacion.save()
        return Response({'mensaje': 'Solicitud de coordinación de retiro rechazada.'}, status=status.HTTP_200_OK)


class ListarSolicitudesAceptadasCoordinacion(APIView):
    """
    Lista todas las solicitudes de coordinación de retiro aceptadas.
    """
    permission_classes = [RutaProtegida(['superadmin', 'coordinadorlogistico'])]
    
    def get(self, request):
        solicitudes = CoordinacionRetiro.objects.filter(estado='aceptado')
        serializer = CoordinacionRetiroSerializer(solicitudes, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
