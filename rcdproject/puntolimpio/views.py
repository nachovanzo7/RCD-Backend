from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import PuntoLimpio
from .serializers import PuntoLimpioSerializer
from usuarios.permisos import RutaProtegida

class CrearPuntoLimpio(APIView):
    """
    Permite registrar un nuevo punto limpio
    """
    permission_classes = [RutaProtegida(['superadmin', 'cliente'])]
    def post(self, request):
        serializer = PuntoLimpioSerializer(data=request.data)
        if serializer.is_valid():
            punto = serializer.save()
            return Response(PuntoLimpioSerializer(punto, context={'request': request}).data,
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ListarPuntosLimpios(APIView):
    """
    Lista todos los puntos limpios
    """
    permission_classes = [RutaProtegida(['superadmin', 'cliente', 'supervisor_obra'])]
    def get(self, request):
        puntos = PuntoLimpio.objects.all()
        serializer = PuntoLimpioSerializer(puntos, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

class ActualizarPuntoLimpio(APIView):
    """
    Permite actualizar un punto limpio existente.
    Se usa PATCH para actualización parcial.
    """
    permission_classes = [RutaProtegida(['superadmin', 'cliente', 'supervisor_obra'])]
    def patch(self, request, pk):
        try:
            punto = PuntoLimpio.objects.get(pk=pk)
        except PuntoLimpio.DoesNotExist:
            return Response({'error': 'Punto limpio no encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = PuntoLimpioSerializer(punto, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)