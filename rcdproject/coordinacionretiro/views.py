from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from .models import CoordinacionRetiro
from .serializers import CoordinacionRetiroSerializer

class CrearCoordinacionRetiro(APIView):
    """
    Registra una nueva coordinación de retiro.
    """
    def post(self, request):
        serializer = CoordinacionRetiroSerializer(data=request.data)
        if serializer.is_valid():
            coordinacion = serializer.save()
            return Response(CoordinacionRetiroSerializer(coordinacion, context={'request': request}).data,
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ListarCoordinacionesRetiro(APIView):
    """
    Lista todas las coordinaciones de retiro.
    """
    def get(self, request):
        coordinaciones = CoordinacionRetiro.objects.all()
        serializer = CoordinacionRetiroSerializer(coordinaciones, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

class ActualizarEstadoCoordinacionRetiro(APIView):
    """
    Actualiza el estado (y opcionalmente la fecha de retiro) de una coordinación.
    Si el estado se actualiza a 'completado', se asigna automáticamente la fecha de retiro actual.
    """
    def put(self, request, pk):
        try:
            coordinacion = CoordinacionRetiro.objects.get(pk=pk)
        except CoordinacionRetiro.DoesNotExist:
            return Response({'error': 'Coordinación no encontrada.'}, status=status.HTTP_404_NOT_FOUND)
        
        data = {}
        if 'estado' in request.data:
            data['estado'] = request.data['estado']
            if request.data['estado'] == 'completado' and 'fecha_retiro' not in request.data:
                data['fecha_retiro'] = timezone.now()
        if 'fecha_retiro' in request.data:
            data['fecha_retiro'] = request.data['fecha_retiro']
        
        serializer = CoordinacionRetiroSerializer(coordinacion, data=data, partial=True)
        if serializer.is_valid():
            coordinacion = serializer.save()
            return Response(CoordinacionRetiroSerializer(coordinacion, context={'request': request}).data,
                            status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)