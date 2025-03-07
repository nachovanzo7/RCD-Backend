from django.shortcuts import render
from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework import status
from .models import SupervisorObra
from .serializers import SupervisorObraSerializer
from usuarios.permisos import RutaProtegida

class CrearSupervisorObra(APIView):
    """
    Permite registrar un nuevo supervisor de obra.
    Se espera que se asocie al usuario correspondiente (deberá crearse previamente o en conjunto).
    """
    permission_classes = [RutaProtegida(['superadmin'])]
    
    def post(self, request):
        serializer = SupervisorObraSerializer(data=request.data)
        if serializer.is_valid():
            supervisor = serializer.save()
            return Response(
                SupervisorObraSerializer(supervisor, context={'request': request}).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from obras.models import Obra
class ListarSupervisoresObra(APIView):
    permission_classes = [RutaProtegida(['superadmin', 'tecnico'])]
    
    def get(self, request, obra_id):
        try:
            obra = Obra.objects.get(pk=obra_id)
            supervisores = SupervisorObra.objects.filter(obra=obra).select_related('usuario')
            serializer = SupervisorObraSerializer(supervisores, many=True)
            return Response(serializer.data)
        except Obra.DoesNotExist:
            return Response(
                {"error": "Obra no encontrada"}, 
                status=status.HTTP_404_NOT_FOUND
            )

class ModificarDatosSupervisorObra(APIView):
    """
    Permite modificar los datos de un supervisor de obra.
    """
    permission_classes = [RutaProtegida(['superadmin', 'supervisor'])]
    
    def patch(self, request, pk):
        try:
            supervisor = SupervisorObra.objects.get(pk=pk)
        except SupervisorObra.DoesNotExist:
            return Response({'error': 'El supervisor de obra no fue encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = SupervisorObraSerializer(supervisor, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EliminarSupervisorObra(APIView):
    """
    Elimina un supervisor de obra.
    """
    permission_classes = [RutaProtegida(['superadmin'])]
    
    def delete(self, request, pk):
        try:
            supervisor = SupervisorObra.objects.get(pk=pk)
        except SupervisorObra.DoesNotExist:
            return Response({'error': 'El supervisor de obra no fue encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        
        supervisor.delete()
        return Response({'mensaje': 'El supervisor de obra fue eliminado.'}, status=status.HTTP_200_OK)

