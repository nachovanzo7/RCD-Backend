from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from .serializers import ActualizarDatosSuperUsuarioSerializer, CrearUsuarioSerializer
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.permissions import IsAuthenticated
from .permisos import RutaProtegida

Usuario = get_user_model()

class ActualizarDatosSuperUsuario(APIView):
    """
    Vista que permite al superusuario modificar su email y contraseña.
    Requiere que el usuario esté autenticado y sea superadministrador.
    """
    permission_classes = [IsAuthenticated]

    def put(self, request):
        usuario = request.user
        if usuario.rol != 'super_administrador':
            return Response(
                {"error": "No tienes permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = ActualizarDatosSuperUsuarioSerializer(instance=usuario, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"mensaje": "Datos actualizados correctamente."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CrearUsuario(APIView):
    """
    Vista que permite al superadministrador crear nuevos usuarios con un rol específico.
    """
    permission_classes = [RutaProtegida(['super_administrador'])]

    def post(self, request):
        serializer = CrearUsuarioSerializer(data=request.data)
        if serializer.is_valid():
            try:
                usuario = serializer.save()
            except DjangoValidationError as e:
                return Response(e.message_dict, status=status.HTTP_400_BAD_REQUEST)
            # Obtenemos o creamos el token para el usuario
            token, created = Token.objects.get_or_create(user=usuario)
            return Response({
                "mensaje": "Usuario creado exitosamente.",
                "usuario": {
                    "username": usuario.username,
                    "email": usuario.email,
                    "rol": usuario.rol,
                    "token": token.key
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    authentication_classes = []  
    permission_classes = []

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        if not email or not password:
            return Response(
                {'error': 'Por favor, ingresa el email y la contraseña.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Buscar el usuario por email
        try:
            user_obj = Usuario.objects.get(email=email)
        except Usuario.DoesNotExist:
            return Response({'error': 'Credenciales inválidas.'}, status=status.HTTP_401_UNAUTHORIZED)
        
        # Si el usuario es un cliente, verificar que su solicitud esté aprobada
        if user_obj.rol == 'cliente':
            try:
                from clientes.models import Cliente
                cliente = Cliente.objects.get(mail=email)
                # Verificar que exista la solicitud y que su estado sea "aceptado"
                if not hasattr(cliente, 'solicitud') or cliente.solicitud.estado != 'aceptado':
                    return Response({'error': 'Acceso denegado. Cliente no aprobado.'}, status=status.HTTP_403_FORBIDDEN)
            except Cliente.DoesNotExist:
                return Response({'error': 'Cliente no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        # Autenticar usando el username real del usuario
        user = authenticate(username=user_obj.username, password=password)
        if user is None:
            return Response({'error': 'Credenciales inválidas.'}, status=status.HTTP_401_UNAUTHORIZED)
        
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'email': user.email,
            'rol': user.rol
        }, status=status.HTTP_200_OK)
