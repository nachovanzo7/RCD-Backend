from django.shortcuts import render
from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework import status
from .models import SupervisorObra
from .serializers import SupervisorObraSerializer

class CrearSupervisorObra(APIView):
    """
    Permite registrar un nuevo supervisor de obra
    """
    def post(self, request):
        serializer = SupervisorObraSerializer(data=request.data)
        if serializer.is_valid():
            supervisor = serializer.save()
            return Response(
                SupervisorObraSerializer(supervisor, context={'request': request}).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ListarSupervisoresObra(APIView):
    """
    Permite listar todos los supervisores de obra
    """
    def get(self, request):
        supervisores = SupervisorObra.objects.all()
        serializer = SupervisorObraSerializer(supervisores, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
