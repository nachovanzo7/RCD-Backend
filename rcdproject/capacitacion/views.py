from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Capacitacion
from .serializers import CapacitacionSerializer

class CrearCapacitacion(APIView):
    """
    Permite registrar una nueva capacitación.
    """
    def post(self, request):
        serializer = CapacitacionSerializer(data=request.data)
        if serializer.is_valid():
            capacitacion = serializer.save()
            return Response(
                CapacitacionSerializer(capacitacion, context={'request': request}).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ListarCapacitaciones(APIView):
    """
    Lista todas las capacitaciones registradas.
    """
    def get(self, request):
        capacitaciones = Capacitacion.objects.all()
        serializer = CapacitacionSerializer(capacitaciones, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

class DetalleCapacitacion(APIView):
    """
    Muestra el detalle de una capacitación específica.
    """
    def get(self, request, pk):
        try:
            capacitacion = Capacitacion.objects.get(pk=pk)
        except Capacitacion.DoesNotExist:
            return Response({'error': 'Capacitación no encontrada.'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = CapacitacionSerializer(capacitacion, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
