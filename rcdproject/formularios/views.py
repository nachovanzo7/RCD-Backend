from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction

# Importa los modelos
from visitas.models import Visita
from condiciondeobras.models import CondicionDeObra
from puntolimpio.models import PuntoLimpio, PuntoAcopio
from materiales.models import Material
from obras.models import Obra
from tecnicos.models import Tecnico

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from .models import Formularios
from .serializers import FormularioSerializer

class CrearFormulario(APIView):
    """
    View para crear un nuevo formulario sin actualizar registros existentes.
    """
    def post(self, request):
        data = request.data  # Data enviada desde el frontend

        try:
            with transaction.atomic():
                # Crear un nuevo formulario con los datos recibidos
                formulario_serializer = FormularioSerializer(data=data)
                
                if formulario_serializer.is_valid():
                    formulario = formulario_serializer.save()
                    
                    return Response(
                        {"mensaje": "Formulario creado exitosamente", "formulario_id": formulario.id},
                        status=status.HTTP_201_CREATED
                    )
                else:
                    return Response(
                        {"error": "Datos inválidos", "detalles": formulario_serializer.errors},
                        status=status.HTTP_400_BAD_REQUEST
                    )

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Formularios
from .serializers import FormularioSerializer

class ListarFormularios(APIView):
    """
    View para listar todos los formularios registrados en la base de datos.
    """
    def get(self, request):
        formularios = Formularios.objects.all()  # Obtiene todos los formularios
        serializer = FormularioSerializer(formularios, many=True)  # Serializa los datos
        return Response(serializer.data, status=status.HTTP_200_OK)
