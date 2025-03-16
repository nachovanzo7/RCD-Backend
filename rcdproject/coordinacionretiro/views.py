from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from .models import CoordinacionRetiro
from .serializers import CoordinacionRetiroSerializer
from rcdproject.usuarios.permisos import RutaProtegida

class CrearCoordinacionRetiro(APIView):
    permission_classes = [RutaProtegida(['superadmin', 'coordinadorlogistico', 'cliente', 'supervisor'])]

    def post(self, request):
        serializer = CoordinacionRetiroSerializer(data=request.data)
        if serializer.is_valid():
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
    permission_classes = [RutaProtegida(['superadmin', 'coordinadorlogistico', 'cliente', 'coordinador', 'supervisor'])]
    
    def get(self, request):
        coordinaciones = CoordinacionRetiro.objects.filter(estado='pendiente')
        serializer = CoordinacionRetiroSerializer(coordinaciones, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class AceptarCoordinacionRetiro(APIView):
    """
    Permite al administrador aceptar una solicitud de coordinación de retir
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
        if 'fecha_retiro' not in request.data:
            coordinacion.fecha_retiro = timezone.now()
        else:
            coordinacion.fecha_retiro = request.data['fecha_retiro']
        coordinacion.save()
        return Response({'mensaje': 'Solicitud de coordinación de retiro aceptada.'}, status=status.HTTP_200_OK)


class RechazarCoordinacionRetiro(APIView):
    """
    Permite al administrador rechazar una solicitud de coordinación de retiro
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


from rcdproject.supervisor_obra.models import SupervisorObra

class ListarSolicitudesAceptadasCoordinacion(APIView):
    """
    Lista todas las solicitudes de coordinacion de retiro aceptadas.
    - Los superadmin, coordinadores y técnicos ven todas.
    - Los supervisores solo ven las coordinaciones de las obras donde están asignados.
    - Los clientes solo ven las coordinaciones de sus propias obras.
    """
    permission_classes = [RutaProtegida(['superadmin', 'coordinadorlogistico', 'cliente', 'coordinador', 'tecnico', 'supervisor'])]

    def get(self, request):
        user = request.user

        # Si es superadmin, coordinador, logístico o técnico, ve todas las coordinaciones aceptadas
        if user.rol in ['superadmin', 'coordinadorlogistico', 'coordinador', 'tecnico']:
            solicitudes = CoordinacionRetiro.objects.filter(estado='aceptado')

        # Si es supervisor, solo ve coordinaciones de las obras donde está asignado
        elif user.rol == 'supervisor':
            try:
                supervisor = SupervisorObra.objects.get(usuario=user)
                solicitudes = CoordinacionRetiro.objects.filter(estado='aceptado', obra__supervisores=supervisor)
            except SupervisorObra.DoesNotExist:
                return Response({"error": "No tienes obras asignadas como supervisor."}, status=status.HTTP_403_FORBIDDEN)

        # Si es cliente, solo ve coordinaciones de sus propias obras
        elif user.rol == 'cliente':
            solicitudes = CoordinacionRetiro.objects.filter(estado='aceptado', obra__cliente=user.cliente)

        # Si no está en ninguno de los roles anteriores, denegar acceso
        else:
            return Response({"error": "No tienes permiso para ver coordinaciones."}, status=status.HTTP_403_FORBIDDEN)

        serializer = CoordinacionRetiroSerializer(solicitudes, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class DetallesCoordinacion(APIView):
    permission_classes = [RutaProtegida(['superadmin', 'coordinadorlogistico', 'cliente', ''])]

    def get(self, request, pk):
        try:
            coordinacion = CoordinacionRetiro.objects.get(pk=pk)
        except CoordinacionRetiro.DoesNotExist:
            return Response({'error': 'Coordinación no encontrada.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = CoordinacionRetiroSerializer(coordinacion, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
from django.shortcuts import get_object_or_404

class ActualizarCoordinacionRetiro(APIView):
    permission_classes = [RutaProtegida(['superadmin', 'coordinadorlogistico', 'cliente'])]

    def patch(self, request, pk):
        # Se obtiene la coordinacion o se lanza 404 si no existe
        coordinacion = get_object_or_404(CoordinacionRetiro, pk=pk)

        # Se instancia el serializer con partial=True para permitir actualizacion parcial
        serializer = CoordinacionRetiroSerializer(
            coordinacion,
            data=request.data,
            partial=True,                # <----- Importante
            context={'request': request}
        )

        if serializer.is_valid():
            coordinacion_actualizada = serializer.save()
            # Retornamos la data actualizada
            return Response(
                CoordinacionRetiroSerializer(coordinacion_actualizada, context={'request': request}).data,
                status=status.HTTP_200_OK
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)