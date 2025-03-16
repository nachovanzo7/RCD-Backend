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
from rcdproject.clientes.models import Cliente
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


# usuarios/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.core.exceptions import ValidationError as DjangoValidationError
from rcdproject.usuarios.permisos import RutaProtegida
from rcdproject.usuarios.serializers import CrearUsuarioSerializer
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny
from rcdproject.obras.models import Obra
from rcdproject.tecnicos.models import Tecnico
from rcdproject.supervisor_obra.models import SupervisorObra

class CrearUsuario(APIView):
    permission_classes = [RutaProtegida(['superadmin'])]

    def post(self, request):

        serializer = CrearUsuarioSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            usuario = serializer.save()
        except DjangoValidationError as e:
            return Response(e.message_dict, status=status.HTTP_400_BAD_REQUEST)

        rol = request.data.get('rol')
        obra_id = request.data.get('obra')

        if rol == 'tecnico' and obra_id:
            try:
                tecnico_obj, created = Tecnico.objects.get_or_create(
                    usuario=usuario,
                    defaults={'nombre': usuario.username}
                )
                obra = Obra.objects.get(pk=obra_id)
                obra.tecnico = tecnico_obj
                obra.save()
            except Obra.DoesNotExist:
                pass
            except Tecnico.DoesNotExist:
                pass

        elif rol == 'supervisor' and obra_id:
            try:
                obra_obj = Obra.objects.get(pk=obra_id)

                sup_obj, created = SupervisorObra.objects.get_or_create(
                    usuario=usuario,
                    defaults={
                        'telefono': '',
                        'obra': obra_obj,
                    }
                )
            except Obra.DoesNotExist:
                pass
            except SupervisorObra.DoesNotExist:
                pass

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


import logging
logger = logging.getLogger(__name__)

@method_decorator(csrf_exempt, name='dispatch')
class LoginView(APIView):
    authentication_classes = []  
    permission_classes = [AllowAny]

    def post(self, request):
        try:
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

            # Verifica si es cliente y si está aprobado (ajusta según tu lógica)
            if user_obj.rol == 'cliente':
                try:
                    cliente = Cliente.objects.get(usuario=user_obj)
                    if not hasattr(cliente, 'solicitud') or cliente.solicitud.estado not in ['aceptado', 'terminado']:
                        return Response({'error': 'Acceso denegado. Cliente no aprobado.'}, status=status.HTTP_403_FORBIDDEN)
                except Cliente.DoesNotExist:
                    return Response({'error': 'Cliente no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

            user = authenticate(request, username=user_obj.email, password=password)
            if user is None:
                return Response({'error': 'Credenciales inválidas.'}, status=status.HTTP_401_UNAUTHORIZED)

            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'email': user.email,
                'rol': user.rol
            }, status=status.HTTP_200_OK)
        except Exception as e:
            logger.exception("Error en LoginView:")
            return Response({'error': 'Error interno en el servidor.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
from rcdproject.tecnicos.models import Tecnico
from rcdproject.supervisor_obra.models import SupervisorObra
class ActualizarUsuario(APIView):
    permission_classes = [RutaProtegida(['superadmin'])]

    def patch(self, request, email):
        try:
            usuario = Usuario.objects.get(email=email)
        except Usuario.DoesNotExist:
            return Response({"error": "Usuario no encontrado."}, status=status.HTTP_404_NOT_FOUND)

        serializer = UsuarioSerializer(usuario, data=request.data, partial=True)

        if serializer.is_valid():
            usuario_actualizado = serializer.save()
            obra = serializer.validated_data.get('obra')

            # Si es técnico, actualiza su obra relacionada
            if usuario_actualizado.rol == 'tecnico':
                tecnico, created = Tecnico.objects.get_or_create(usuario=usuario_actualizado)
                if obra:
                    obra.tecnico = tecnico
                    obra.save()

            # Si es supervisor, actualiza la relación en la app SupervisorObra
            elif usuario_actualizado.rol == 'supervisor':
                supervisor, created = SupervisorObra.objects.get_or_create(usuario=usuario_actualizado, defaults={
                    'telefono': '',
                    'nivel_capacitacion': 'no_hay',
                    'obra': obra
                })
                if not created and obra:
                    supervisor.obra = obra
                    supervisor.save()

            return Response({
                "mensaje": "Usuario actualizado correctamente.",
                "usuario": UsuarioSerializer(usuario_actualizado).data
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

Usuario = get_user_model()
from rcdproject.usuarios.serializers import UsuarioSerializer

class ListarUsuarios(APIView):
    permission_classes = [RutaProtegida(['superadmin'])]

    def get(self, request):
        usuarios = Usuario.objects.all()
        serializer = UsuarioSerializer(usuarios, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

