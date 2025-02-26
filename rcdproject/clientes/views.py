from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from usuarios.permisos import RutaProtegida
from rest_framework import status
from django.utils import timezone
from .models import Cliente, SolicitudCliente
from .serializers import ClienteSerializer, SolicitudClienteSerializer, SolicitudClienteAdminSerializer
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

Usuario = get_user_model()

class RegistroCliente(APIView):
    """
    Permite que el cliente se registre y envíe una solicitud para aprobación.
    """
    permission_classes = [RutaProtegida(['super_administrador'])]
    
    def post(self, request):
        serializer_cliente = ClienteSerializer(data=request.data)
        if serializer_cliente.is_valid():
            cliente = serializer_cliente.save()
            # Se crea la solicitud con estado por defecto "pendiente"
            solicitud = SolicitudCliente.objects.create(cliente=cliente)
            return Response({
                'mensaje': 'Cliente registrado, pendiente de aprobación.',
                'cliente': ClienteSerializer(cliente).data,
                'solicitud': SolicitudClienteSerializer(solicitud).data,
            }, status=status.HTTP_201_CREATED)
        return Response(serializer_cliente.errors, status=status.HTTP_400_BAD_REQUEST)

class ListarSolicitudesCliente(APIView):
    """
    Lista todas las solicitudes de clientes para revisión del administrador.
    """
    permission_classes = [RutaProtegida(['super_administrador'])]

    def get(self, request):
        solicitudes = SolicitudCliente.objects.all()
        serializer = SolicitudClienteAdminSerializer(solicitudes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class AprobarSolicitudCliente(APIView):
    """
    Permite al administrador aprobar una solicitud.
    """
    permission_classes = [RutaProtegida(['super_administrador'])]
    
    def put(self, request, pk):
        try:
            solicitud = SolicitudCliente.objects.get(pk=pk)
        except SolicitudCliente.DoesNotExist:
            return Response({'error': 'Solicitud no encontrada.'}, status=status.HTTP_404_NOT_FOUND)
        
        if solicitud.estado != 'pendiente':
            return Response({'error': 'La solicitud ya ha sido procesada.'}, status=status.HTTP_400_BAD_REQUEST)
        
        solicitud.estado = 'aceptado'
        solicitud.fecha_solicitud = timezone.now()
        solicitud.save()
        
        # Obtenemos el usuario asociado al cliente a través del email.
        try:
            usuario = Usuario.objects.get(email=solicitud.cliente.mail)
        except Usuario.DoesNotExist:
            return Response({'error': 'Usuario asociado no encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        
        # Generamos o obtenemos el token para el usuario
        token, created = Token.objects.get_or_create(user=usuario)
        
        return Response({
            'mensaje': 'Solicitud aprobada. El usuario tiene rol \"cliente\".',
            'token': token.key
        }, status=status.HTTP_200_OK)

class RechazarSolicitudCliente(APIView):
    """
    Permite al administrador rechazar una solicitud.
    """
    permission_classes = [RutaProtegida(['super_administrador'])]
    
    def put(self, request, pk):
        try:
            solicitud = SolicitudCliente.objects.get(pk=pk)
        except SolicitudCliente.DoesNotExist:
            return Response({'error': 'Solicitud no encontrada.'}, status=status.HTTP_404_NOT_FOUND)
        
        if solicitud.estado != 'pendiente':
            return Response({'error': 'La solicitud ya ha sido procesada.'}, status=status.HTTP_400_BAD_REQUEST)
        
        solicitud.estado = 'rechazado'
        solicitud.save()
        
        return Response({'mensaje': 'La solicitud fue rechazada.'}, status=status.HTTP_200_OK)

class ListarClientesAprobados(APIView):
    """
    Lista todos los clientes cuya solicitud fue aceptada.
    """
    permission_classes = [RutaProtegida(['super_administrador', 'coordinador_obra', 'coordinador_retiro'])]
    
    def get(self, request):
        clientes_aprobados = Cliente.objects.filter(solicitud__estado='aceptado')
        serializer = ClienteSerializer(clientes_aprobados, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class DetalleCliente(APIView):
    """
    Devuelve la información de un cliente si su solicitud está aprobada.
    """
    permission_classes = [RutaProtegida(['super_administrador', 'coordinador_obra'])]
    
    def get(self, request, pk):
        try:
            cliente = Cliente.objects.get(pk=pk)
        except Cliente.DoesNotExist:
            return Response({'error': 'Cliente no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        if cliente.solicitud.estado != 'aceptado':
            return Response({'error': 'El cliente no está registrado (estado pendiente o rechazado).'}, 
                            status=status.HTTP_403_FORBIDDEN)
        
        serializer = ClienteSerializer(cliente, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

class ActualizarCliente(APIView):
    """
    Permite actualizar los datos de un cliente.
    """
    permission_classes = [RutaProtegida(['super_administrador', 'cliente'])]
    
    def patch(self, request, pk):
        try:
            cliente = Cliente.objects.get(pk=pk)
        except Cliente.DoesNotExist:
            return Response({'error': 'Cliente no encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ClienteSerializer(cliente, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
