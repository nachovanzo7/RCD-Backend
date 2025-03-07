from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Capacitacion
from .serializers import CapacitacionSerializer
from supervisor_obra.models import SupervisorObra
from django.core.exceptions import ObjectDoesNotExist

class CrearCapacitacion(APIView):
    """
    Permite registrar una nueva capacitación, recibiendo por ejemplo
    'supervisor_email' en el request y asignándolo como supervisor.
    """

    def post(self, request):
        data = request.data.copy()

        serializer = CapacitacionSerializer(data=data)
        if serializer.is_valid():
            supervisor_email = data.get('supervisor_email')
            if supervisor_email:
                try:
                    # Buscamos un SupervisorObra cuyo usuario tenga este email
                    supervisor = SupervisorObra.objects.get(usuario__email=supervisor_email)
                    # Creamos la capacitación con ese supervisor
                    capacitacion = serializer.save(supervisor=supervisor)
                except (SupervisorObra.DoesNotExist, ObjectDoesNotExist):
                    return Response(
                        {"error": f"No se encontró un supervisor con el email {supervisor_email}."},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            else:
                capacitacion = serializer.save()

            return Response(
                CapacitacionSerializer(capacitacion).data,
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ListarCapacitaciones(APIView):
    """
    Lista todas las capacitaciones registradas.
    """
    def get(self, request):
        capacitaciones = Capacitacion.objects.all()
        serializer = CapacitacionSerializer(capacitaciones, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

class DetalleCapacitacion(APIView):
    """
    Muestra el detalle de una capacitación específica.
    """
    def get(self, request, pk):
        try:
            capacitacion = Capacitacion.objects.get(pk=pk)
        except Capacitacion.DoesNotExist:
            return Response({'error': 'Capacitación no encontrada.'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = CapacitacionSerializer(capacitacion, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
