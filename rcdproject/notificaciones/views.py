from rest_framework.decorators import api_view
from rest_framework.response import Response
from notificaciones.models import Notificacion
from .serializers import NotificacionSerializer

@api_view(['GET'])
def lista_notificaciones(request, cliente_id):
    """
    Retorna las notificaciones del cliente.
    """
    notificaciones = Notificacion.objects.filter(cliente__id=cliente_id).order_by('-created_at')
    serializer = NotificacionSerializer(notificaciones, many=True)
    return Response(serializer.data)
