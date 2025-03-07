from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from .models import Formularios
from .serializers import FormularioSerializer

class CrearFormulario(APIView):
    """
    View para crear un nuevo formulario sin actualizar registros existentes.
    """
    def post(self, request):
        data = request.data 
        try:
            with transaction.atomic():
                serializer = FormularioSerializer(data=data)
                if serializer.is_valid():
                    formulario = serializer.save()
                    return Response(
                        {"mensaje": "Formulario creado exitosamente", "formulario_id": formulario.id},
                        status=status.HTTP_201_CREATED
                    )
                else:
                    return Response(
                        {"error": "Datos inválidos", "detalles": serializer.errors},
                        status=status.HTTP_400_BAD_REQUEST
                    )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ListarFormularios(APIView):
    """
    View para listar los formularios. Si el usuario es técnico, se muestran solo los vinculados a él.
    """
    def get(self, request):
        user = request.user
        if user.rol == 'tecnico':
            formularios = Formularios.objects.filter(tecnico__usuario=user)
        else:
            formularios = Formularios.objects.all()
        serializer = FormularioSerializer(formularios, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DetalleFormulario(generics.RetrieveAPIView):
    """
    Endpoint que devuelve el detalle de un formulario dado su id
    """
    queryset = Formularios.objects.all()
    serializer_class = FormularioSerializer
    permission_classes = [IsAuthenticated]
