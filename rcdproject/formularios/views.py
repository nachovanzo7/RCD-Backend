from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError as DjangoValidationError
from .serializers import FormularioSerializer

class CrearFormulario(APIView):
    """
    Permite crear un nuevo registro de Formulario.
    """
    def post(self, request):
        serializer = FormularioSerializer(data=request.data)
        if serializer.is_valid():
            try:
                formulario = serializer.save()
            except DjangoValidationError as e:
                return Response(e.message_dict, status=status.HTTP_400_BAD_REQUEST)
            return Response(FormularioSerializer(formulario, context={'request': request}).data,
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
