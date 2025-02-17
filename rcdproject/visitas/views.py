from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Visita
from .serializers import VisitaSerializer

class CrearVisita(APIView):
    """
    Permite registrar una nueva visita a una obra.
    """
    def post(self, request):
        serializer = VisitaSerializer(data=request.data)
        if serializer.is_valid():
            visita = serializer.save()
            return Response(
                VisitaSerializer(visita, context={'request': request}).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ListarVisitas(APIView):
    """
    Lista todas las visitas registradas.
    """
    def get(self, request):
        visitas = Visita.objects.all()
        serializer = VisitaSerializer(visitas, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
