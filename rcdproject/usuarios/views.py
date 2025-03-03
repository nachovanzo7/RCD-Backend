from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from .serializers import ActualizarDatosSuperUsuarioSerializer, CrearUsuarioSerializer
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from .permisos import RutaProtegida
from clientes.models import Cliente
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


Usuario = get_user_model()


class ActualizarDatosSuperUsuario(APIView):
    """
    Permite al superusuario modificar su email y contraseña.
    Requiere autenticación y rol 'superadmin'.
    """
    permission_classes = [IsAuthenticated]

    def put(self, request):
        usuario = request.user
        if usuario.rol != 'superadmin':
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
    Permite al superadministrador crear nuevos usuarios con un rol específico.
    """
    permission_classes = [RutaProtegida(['superadmin'])]

    def post(self, request):
        serializer = CrearUsuarioSerializer(data=request.data)
        if serializer.is_valid():
            try:
                usuario = serializer.save()
            except DjangoValidationError as e:
                return Response(e.message_dict, status=status.HTTP_400_BAD_REQUEST)
            token, _ = Token.objects.get_or_create(user=usuario)
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


@method_decorator(csrf_exempt, name='dispatch')
class LoginView(APIView):
    authentication_classes = []  
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        if not email or not password:
            return Response(
                {'error': 'Por favor, ingresa el email y la contraseña.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            user_obj = Usuario.objects.get(email=email)
        except Usuario.DoesNotExist:
            return Response({'error': 'Credenciales inválidas.'}, status=status.HTTP_401_UNAUTHORIZED)
        
        if user_obj.rol == 'cliente':
            try:
                cliente = Cliente.objects.get(usuario=user_obj)
                if not hasattr(cliente, 'solicitud') or cliente.solicitud.estado != 'aceptado':
                    return Response({'error': 'Acceso denegado. Cliente no aprobado.'}, status=status.HTTP_403_FORBIDDEN)
            except Cliente.DoesNotExist:
                return Response({'error': 'Cliente no encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        
        user = authenticate(username=user_obj.username, password=password)
        if user is None:
            return Response({'error': 'Credenciales inválidas.'}, status=status.HTTP_401_UNAUTHORIZED)
        
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'email': user.email,
            'rol': user.rol
        }, status=status.HTTP_200_OK)