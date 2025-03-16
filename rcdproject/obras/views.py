from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from django.core.exceptions import ValidationError
from rcdproject.obras.models import Obra, SolicitudObra, ArchivoObra
from rcdproject.obras.serializers import ObraSerializer, SolicitudObraSerializer, SolicitudObraAdminSerializer
from rcdproject.clientes.models import Cliente
from rcdproject.puntolimpio.models import PuntoLimpio
from rcdproject.materiales.models import Material
from rcdproject.usuarios.permisos import RutaProtegida
from rcdproject.transportistas.models import Transportista

class RegistroObra(APIView):
    """
    Permite al cliente registrar una obra y los archivos adjuntos.
    """
    permission_classes = [RutaProtegida(['superadmin', 'cliente'])]

    def post(self, request):
        serializer_obra = ObraSerializer(data=request.data)
        if serializer_obra.is_valid():
            obra = serializer_obra.save()

            # Procesar y guardar los archivos enviados
            archivos = request.FILES.getlist("archivo")
            for file in archivos:
                ArchivoObra.objects.create(obra=obra, archivo=file)

            # Crear la solicitud de obra con estado "pendiente"
            solicitud = SolicitudObra.objects.create(obra=obra)
            cliente = Cliente.objects.get(pk=obra.cliente.id)
            
            return Response({
                'mensaje': 'Obra registrada, pendiente de aprobacion.',
                'obra': ObraSerializer(obra, context={'request': request}).data,
                'solicitud': SolicitudObraSerializer(solicitud, context={'request': request}).data,
                'ID de cliente': cliente.id
            }, status=status.HTTP_201_CREATED)
        return Response(serializer_obra.errors, status=status.HTTP_400_BAD_REQUEST)


class ListarSolicitudesObra(APIView):
    """
    Lista todas las solicitudes de obras para el administrador
    """
    permission_classes = [RutaProtegida(['superadmin', 'coordinador', 'coordinadorlogistico'])]
    def get(self, request):
        solicitudes = SolicitudObra.objects.all()
        serializer = SolicitudObraAdminSerializer(solicitudes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class AprobarSolicitudObra(APIView):
    """
    Permite al administrador aceptar una solicitud de obra
    """
    permission_classes = [RutaProtegida(['superadmin', 'coordinador', 'coordinadorlogistico'])]
    def put(self, request, pk):
        try:
            solicitud = SolicitudObra.objects.get(pk=pk)
        except SolicitudObra.DoesNotExist:
            return Response({'error': 'Su solicitud no fue encontrada.'}, status=status.HTTP_404_NOT_FOUND)
        
        if solicitud.estado != 'pendiente':
            return Response({'error': 'La solicitud ya ha sido procesada.'}, status=status.HTTP_400_BAD_REQUEST)
        
        solicitud.estado = 'aceptado'
        solicitud.fecha_solicitud = timezone.now()
        solicitud.save()
        return Response({'mensaje': 'Su solicitud de obra fue aprobada.'}, status=status.HTTP_200_OK)

class RechazarSolicitudObra(APIView):
    """
    Permite al administrador rechazar una solicitud de obra
    """
    permission_classes = [RutaProtegida(['superadmin'])]
    def put(self, request, pk):
        try:
            solicitud = SolicitudObra.objects.get(pk=pk)
        except SolicitudObra.DoesNotExist:
            return Response({'error': 'Su solicitud no fue encontrada.'}, status=status.HTTP_404_NOT_FOUND)
        
        if solicitud.estado != 'pendiente':
            return Response({'error': 'La solicitud ya ha sido procesada.'}, status=status.HTTP_400_BAD_REQUEST)
        
        solicitud.estado = 'rechazado'
        solicitud.save()
        
        obra = solicitud.obra
        obra.puntos_limpios.all().delete()
        obra.materiales.all().delete()
        
        return Response(
            {'mensaje': 'Su solicitud de obra fue rechazada y se eliminaron los puntos limpios y materiales asociados.'},
            status=status.HTTP_200_OK
        )

class ListarObrasAprobadas(APIView):
    """
    Muestra una lista con las obras que fueron aprobadas
    """
    permission_classes = [RutaProtegida(['superadmin', 'cliente', 'coordinador', 'coordinadorlogistico', 'tecnico', 'supervisor'])]
    def get(self, request):
        obras = Obra.objects.filter(solicitud__estado__in=['aceptado', 'terminado'])
        serializer = ObraSerializer(obras, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DetallesObra(APIView):
    """
    Muestra los detalles de una obra
    """
    permission_classes = [RutaProtegida(['superadmin', 'coordinador', 'cliente', 'tecnico', 'coordinadorlogistico'])]

    def get(self, request, pk):
        try:
            obra = Obra.objects.get(pk=pk)
        except Obra.DoesNotExist:
            return Response({'error': 'Obra no encontrada.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ObraSerializer(obra, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

class EliminarObra(APIView):
    """
    Eliminar una obra
    """
    permission_classes = [RutaProtegida(['superadmin', 'cliente'])]
    def delete(self, request, pk):
        try:
            obra = Obra.objects.get(pk=pk)
        except Obra.DoesNotExist:
            return Response({'error': 'Obra no encontrada.'}, status=status.HTTP_404_NOT_FOUND)
        
        obra.delete()
        return Response({'mensaje': 'Obra eliminada.'}, status=status.HTTP_200_OK)
    
class ActualizarObra(APIView):
    """
    Permite actualizar los datos de una obra.
    """
    permission_classes = [RutaProtegida(['superadmin', 'cliente'])]

    def patch(self, request, pk):
        try:
            obra = Obra.objects.get(pk=pk)
        except Obra.DoesNotExist:
            return Response({'error': 'Obra no encontrada.'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ObraSerializer(obra, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            obra_actualizada = serializer.save()
            return Response(ObraSerializer(obra_actualizada, context={'request': request}).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class MarcarObraTerminada(APIView):
    """
    Vista para marcar una obra como terminada.
    """
    permission_classes = [RutaProtegida(['superadmin', 'coordinador', 'coordinadorlogistico', 'tecnico'])]

    def put(self, request, pk):
        """
        Actualiza el estado de la solicitud de una obra a 'terminado'.
        Se espera que se reciba el identificador (pk) de la obra en la URL.
        """
        try:
            obra = Obra.objects.get(pk=pk)
        except Obra.DoesNotExist:
            return Response({"error": "Obra no encontrada."}, status=status.HTTP_404_NOT_FOUND)
        
        # Accedemos a la solicitud de obra a través del related_name 'solicitud'
        solicitud = obra.solicitud
        
        # Opcional: Verificar si la obra ya se encuentra terminada
        if solicitud.estado == 'terminado':
            return Response({"mensaje": "La obra ya se encuentra terminada."}, status=status.HTTP_400_BAD_REQUEST)
        
        solicitud.estado = 'terminado'
        solicitud.save()
        return Response({"mensaje": "Obra marcada como terminada."}, status=status.HTTP_200_OK)
    
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

class ListarObraPorCliente(generics.ListAPIView):
    serializer_class = ObraSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.rol == 'cliente':
            return Obra.objects.filter(cliente__usuario__email=user.email)
        return Obra.objects.none()

from rcdproject.supervisor_obra.serializers import SupervisorObraSerializer

class SupervisoresDeObra(APIView):
    """
    Devuelve el supervisor vinculado a la obra (o lista vacía si no hay).
    Como la relacion es OneToOne, solo habrá 1 o ninguno.
    """
    permission_classes = [RutaProtegida([
        'superadmin', 
        'coordinador', 
        'coordinadorlogistico',
        'tecnico',
        'supervisor',
        'cliente'
    ])]

    def get(self, request, pk):
        try:
            obra = Obra.objects.get(pk=pk)
        except Obra.DoesNotExist:
            return Response({"error": "Obra no encontrada."}, status=status.HTTP_404_NOT_FOUND)
        
        # Si la obra no tiene supervisor, la relacion OneToOne puede no existir
        if not hasattr(obra, 'supervisor'):
            return Response([], status=status.HTTP_200_OK)
        
        # En tu modelo, la relacion se llama 'supervisor'
        sup = obra.supervisor  
        serializer = SupervisorObraSerializer(sup) 
        # Retornamos un array con un solo elemento para que el frontend maneje un array
        return Response([serializer.data], status=status.HTTP_200_OK)