from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Transportista
from .serializers import TransportistaSerializer

class CrearTransportista(APIView):
    """
    Permite al coordinador (administrador) dar de alta un transportista.
    """
    def post(self, request):
        serializer = TransportistaSerializer(data=request.data)
        if serializer.is_valid():
            transportista = serializer.save()
            # Se agrega el contexto para que el serializer pueda construir los hiperlinks correctamente.
            return Response(
                TransportistaSerializer(transportista, context={'request': request}).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ListarTransportistas(APIView):
    """
    Lista todos los transportistas.
    """
    def get(self, request):
        transportistas = Transportista.objects.all()
        serializer = TransportistaSerializer(transportistas, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

class ModificarDatosTransportista(APIView):
    """
    Permite modificar los datos de un transportista
    """
    def patch(self, request, pk):
        try:
            transportista = Transportista.objects.get(pk=pk)
        except Transportista.DoesNotExist:
            return Response({'error': 'El transportista no fue encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = TransportistaSerializer(transportista, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
