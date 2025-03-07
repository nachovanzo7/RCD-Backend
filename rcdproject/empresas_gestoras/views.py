from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import EmpresaGestora
from .serializers import EmpresaGestoraSerializer
from usuarios.permisos import RutaProtegida 

class CrearEmpresaGestora(APIView):
    """
    Permite registrar una nueva empresa gestora.
    """
    permission_classes = [RutaProtegida(['superadmin', 'coordinadorlogistico'])]
    
    def post(self, request):
        serializer = EmpresaGestoraSerializer(data=request.data)
        if serializer.is_valid():
            empresa = serializer.save()
            return Response(
                EmpresaGestoraSerializer(empresa, context={'request': request}).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ListarEmpresasGestoras(APIView):
    """
    Lista todas las empresas gestoras.
    """
    permission_classes = [RutaProtegida(['superadmin', 'coordinadorlogistico', 'cliente', 'supervisor'])]
    
    def get(self, request):
        empresas = EmpresaGestora.objects.all()
        serializer = EmpresaGestoraSerializer(empresas, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

class DetalleEmpresaGestora(APIView):
    """
    Devuelve los detalles de una empresa gestora.
    """
    permission_classes = [RutaProtegida(['superadmin', 'coordinadorlogistico'])]
    
    def get(self, request, pk):
        try:
            empresa = EmpresaGestora.objects.get(pk=pk)
        except EmpresaGestora.DoesNotExist:
            return Response({'error': 'La empresa gestora no fue encontrada.'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = EmpresaGestoraSerializer(empresa, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

class ModificarDatosEmpresaGestora(APIView):
    """
    Permite modificar los datos de una empresa gestora.
    """
    permission_classes = [RutaProtegida(['superadmin', 'coordinadorlogistico'])]
    
    def patch(self, request, pk):
        try:
            empresa = EmpresaGestora.objects.get(pk=pk)
        except EmpresaGestora.DoesNotExist:
            return Response({'error': 'La empresa gestora no fue encontrada.'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = EmpresaGestoraSerializer(empresa, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EliminarEmpresaGestora(APIView):
    """
    Elimina a una empresa gestora.
    """
    permission_classes = [RutaProtegida(['superadmin', 'coordinadorlogistico'])]
    
    def delete(self, request, pk):
        try:
            empresa = EmpresaGestora.objects.get(pk=pk)
        except EmpresaGestora.DoesNotExist:
            return Response({'error': 'La empresa gestora no fue encontrada.'}, status=status.HTTP_404_NOT_FOUND)
        
        empresa.delete()
        return Response({'mensaje': 'La empresa gestora fue eliminada.'}, status=status.HTTP_200_OK)
