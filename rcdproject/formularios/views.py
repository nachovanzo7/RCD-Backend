from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError as DjangoValidationError
from .serializers import FormularioSerializer
from notificaciones.models import Notificacion

class CrearFormulario(APIView):
    """
    Permite crear un nuevo registro de Formulario y, en caso de valores críticos,
    crea una notificación para el cliente asociado a la obra.
    """
    def post(self, request):
        serializer = FormularioSerializer(data=request.data)
        if serializer.is_valid():
            try:
                formulario = serializer.save()
            except DjangoValidationError as e:
                return Response(e.message_dict, status=status.HTTP_400_BAD_REQUEST)
            
            # Diccionario que mapea cada campo con su valor crítico y el nombre del material
            condiciones = {
                'escombro_limpio_observaciones': ('lleno', 'escombro'),
                'plastico_observaciones': ('lleno', 'plástico'),
                'papel_y_carton_observaciones': ('lleno', 'papel y cartón'),
                'metales_observaciones': ('mucha_cantidad', 'metales'),
                'madera_observaciones': ('mucha_cantidad', 'madera'),
                'mezclados_observaciones': ('mucha_cantidad', 'mezclados'),
                'peligrosos_observaciones': ('tanque_lleno', 'peligrosos')
            }
            
            # Construir la lista de materiales críticos
            materiales_criticos = []
            for campo, (valor_critico, nombre_material) in condiciones.items():
                if getattr(formulario, campo) == valor_critico:
                    materiales_criticos.append(nombre_material)
            
            # Si se encontraron materiales críticos, crear la notificación
            if materiales_criticos:
                mensaje = f"Se recomienda coordinar retiro de {', '.join(materiales_criticos)} en la obra \'{formulario.obra.nombre_obra}\'"
                Notificacion.objects.create(cliente=formulario.obra.cliente, mensaje=mensaje)
            
            return Response(FormularioSerializer(formulario, context={'request': request}).data,
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
