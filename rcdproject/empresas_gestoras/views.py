from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import EmpresaGestora
from .serializers import EmpresaGestoraSerializer

class CrearEmpresaGestora(APIView):
    """
    Permite registrar una nueva empresa gestora.
    """
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
    def get(self, request):
        empresas = EmpresaGestora.objects.all()
        serializer = EmpresaGestoraSerializer(empresas, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
