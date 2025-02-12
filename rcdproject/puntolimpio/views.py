from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import PuntoLimpio
from .serializers import PuntoLimpioSerializer

class CrearPuntoLimpio(APIView):
    """
    Permite registrar un nuevo punto limpio
    """
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
    def get(self, request):
        puntos = PuntoLimpio.objects.all()
        serializer = PuntoLimpioSerializer(puntos, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
