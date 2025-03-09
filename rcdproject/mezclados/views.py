from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Mezclado
import traceback
from .serializers import MezcladoSerializer
from usuarios.permisos import RutaProtegida

class RegistrarMezclado(APIView):
    permission_classes = [RutaProtegida(['superadmin', 'coordinador', 'coordinadorlogistico', 'supervisor'])]

    def post(self, request):
        try:
            serializer = MezcladoSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                mezclado = serializer.save()
                return Response(
                    MezcladoSerializer(mezclado, context={'request': request}).data,
                    status=status.HTTP_201_CREATED
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            tb = traceback.format_exc()
            return Response(
                {"error": str(e), "traceback": tb},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class ListarMezclado(APIView):
    """
    Lista todos los registros de Mezclado.
    """
    permission_classes = [RutaProtegida(['superadmin', 'cliente', 'coordinadorlogistico', 'supervisor', 'coordinador'])]

    def get(self, request):
        mezclados = Mezclado.objects.all()
        serializer = MezcladoSerializer(mezclados, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

class MezcladoDetalle(APIView):
    """
    Endpoint para obtener los detalles de un Mezclado.
    Se espera recibir el parámetro 'id' en la query string.
    """
    permission_classes = [RutaProtegida(['superadmin', 'coordinador', 'coordinadorlogistico', 'cliente', 'supervisor'])]

    def get(self, request):
        mezclado_id = request.query_params.get('id')
        if not mezclado_id:
            return Response({"error": "El parámetro 'id' es requerido."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            mezclado = Mezclado.objects.get(id=mezclado_id)
        except Mezclado.DoesNotExist:
            return Response({"error": "Mezclado no encontrado."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            tb = traceback.format_exc()
            return Response({"error": str(e), "traceback": tb}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        serializer = MezcladoSerializer(mezclado, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)