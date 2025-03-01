from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from usuarios.permisos import RutaProtegida
from rest_framework import status
from django.utils import timezone
from rest_framework.permissions import AllowAny, IsAuthenticated
import secrets

from .models import Cliente, SolicitudCliente
from .serializers import (
    ClienteSerializer,
    SolicitudClienteSerializer,
    SolicitudClienteAdminSerializer,
)
from django.contrib.auth import get_user_model, authenticate
from rest_framework.authtoken.models import Token
from django.core.exceptions import ValidationError as DjangoValidationError

Usuario = get_user_model()

class RegistroCliente(APIView):
    """
    Permite que el superadministrador (o el propio usuario en un registro público) cree un nuevo cliente.
    Se crea primero el Usuario con rol 'cliente' y luego se asocia en Cliente.
    Si el email ya existe, se retorna un error.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        raw_password = request.data.get('password') or secrets.token_urlsafe(16)
        email = request.data.get('email')
        nombre = request.data.get('nombre')
        username = request.data.get('username') or nombre

        # Si ya existe un usuario con ese email, devolver error.
        if Usuario.objects.filter(email=email).exists():
            return Response({"error": "El email ya está registrado."}, status=status.HTTP_400_BAD_REQUEST)
        
        usuario = Usuario.objects.create_user(
            username=username,
            email=email,
            password=raw_password,
            first_name=nombre,
            rol='cliente'
        )

        # Inyectar la referencia al usuario en los datos del cliente
        data_cliente = request.data.copy()
        data_cliente['usuario'] = usuario.id

        serializer_cliente = ClienteSerializer(data=data_cliente)
        if serializer_cliente.is_valid():
            cliente = serializer_cliente.save()
            # Crear solicitud con estado "pendiente"
            SolicitudCliente.objects.create(cliente=cliente)
            # Generar o obtener el token
            token, _ = Token.objects.get_or_create(user=usuario)
            return Response({
                'mensaje': 'Cliente registrado, pendiente de aprobación.',
                'cliente': ClienteSerializer(cliente).data,
                'solicitud': SolicitudClienteSerializer(cliente.solicitud).data,
                'token': token.key
            }, status=status.HTTP_201_CREATED)
        return Response(serializer_cliente.errors, status=status.HTTP_400_BAD_REQUEST)


class ListarSolicitudesCliente(APIView):
    """
    Lista todas las solicitudes de clientes para revisión del administrador.
    """
    permission_classes = [RutaProtegida(['superadmin'])]

    def get(self, request):
        solicitudes = SolicitudCliente.objects.all()
        serializer = SolicitudClienteAdminSerializer(solicitudes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AprobarSolicitudCliente(APIView):
    """
    Permite al administrador aprobar una solicitud.
    """
    permission_classes = [RutaProtegida(['superadmin'])]
    
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
        
        # Obtener el usuario asociado al cliente vía la relación
        try:
            usuario = solicitud.cliente.usuario
        except Usuario.DoesNotExist:
            return Response({'error': 'Usuario asociado no encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        
        token, _ = Token.objects.get_or_create(user=usuario)
        
        return Response({
            'mensaje': "Solicitud aprobada. El usuario tiene rol 'cliente'.",
            'token': token.key
        }, status=status.HTTP_200_OK)


class RechazarSolicitudCliente(APIView):
    """
    Permite al administrador rechazar una solicitud y eliminar el usuario asociado.
    """
    permission_classes = [RutaProtegida(['superadmin'])]
    
    def put(self, request, pk):
        try:
            solicitud = SolicitudCliente.objects.get(pk=pk)
        except SolicitudCliente.DoesNotExist:
            return Response({'error': 'Solicitud no encontrada.'}, status=status.HTTP_404_NOT_FOUND)
        
        if solicitud.estado != 'pendiente':
            return Response({'error': 'La solicitud ya ha sido procesada.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Obtener el Cliente usando el identificador almacenado en cliente_id
        try:
            cliente = Cliente.objects.get(pk=solicitud.cliente_id)
        except Cliente.DoesNotExist:
            return Response({'error': 'Cliente no encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        
        usuario = cliente.usuario
        
        # Eliminar primero la solicitud, luego el cliente y finalmente el usuario
        solicitud.delete()
        cliente.delete()
        usuario.delete()
        
        return Response({'mensaje': 'La solicitud fue rechazada y el usuario fue eliminado.'}, status=status.HTTP_200_OK)





class ListarClientesAprobados(APIView):
    """
    Lista todos los clientes cuya solicitud fue aceptada.
    """
    permission_classes = [RutaProtegida(['superadmin', 'coordinador', 'coordinadorlogistico'])]
    
    def get(self, request):
        clientes_aprobados = Cliente.objects.filter(solicitud__estado='aceptado')
        serializer = ClienteSerializer(clientes_aprobados, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DetalleCliente(APIView):
    """
    Devuelve la información de un cliente si su solicitud está aprobada.
    """
    permission_classes = [RutaProtegida(['superadmin', 'coordinador'])]
    
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
    permission_classes = [RutaProtegida(['superadmin', 'cliente'])]
    
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


class EliminarCliente(APIView):
    """
    Permite eliminar un cliente.
    """
    permission_classes = [RutaProtegida(['superadmin'])]
    
    def delete(self, request, pk):
        try:
            cliente = Cliente.objects.get(pk=pk)
        except Cliente.DoesNotExist:
            return Response({'error': 'Cliente no encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        
        cliente.delete()
        return Response({'mensaje': 'Cliente eliminado.'}, status=status.HTTP_200_OK)
