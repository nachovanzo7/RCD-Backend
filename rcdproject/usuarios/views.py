import logging
from django.utils import timezone
from django.contrib.auth import authenticate, get_user_model
from django.core.exceptions import ValidationError as DjangoValidationError
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token

from rcdproject.usuarios.permisos import RutaProtegida
from rcdproject.usuarios.serializers import (
    ActualizarDatosSuperUsuarioSerializer,
    CrearUsuarioSerializer,
    UsuarioSerializer
)
from rcdproject.clientes.models import Cliente, SolicitudCliente
from rcdproject.obras.models import Obra
from rcdproject.tecnicos.models import Tecnico
from rcdproject.supervisor_obra.models import SupervisorObra

Usuario = get_user_model()
logger = logging.getLogger(__name__)


class ActualizarDatosSuperUsuario(APIView):
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
    permission_classes = [RutaProtegida(['superadmin'])]

    def post(self, request):
        serializer = CrearUsuarioSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            usuario = serializer.save()
        except DjangoValidationError as e:
            return Response(e.message_dict, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.exception("Error al crear usuario:")
            return Response({'error': 'Error interno al crear el usuario.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        rol = request.data.get('rol')
        obra_id = request.data.get('obra')

        try:
            if rol == 'tecnico' and obra_id:
                tecnico, _ = Tecnico.objects.get_or_create(usuario=usuario, defaults={'nombre': usuario.username})
                obra = Obra.objects.get(pk=obra_id)
                obra.tecnico = tecnico
                obra.save()

            elif rol == 'supervisor' and obra_id:
                obra = Obra.objects.get(pk=obra_id)
                SupervisorObra.objects.get_or_create(
                    usuario=usuario,
                    defaults={'telefono': '', 'obra': obra}
                )

            elif rol == 'cliente':
                cliente, _ = Cliente.objects.get_or_create(
                    usuario=usuario,
                    defaults={
                        'nombre': usuario.username,
                        'direccion': '',
                        'contacto': '',
                        'nombre_contacto': '',
                        'fecha_ingreso': timezone.now().date(),
                        'razon_social': '',
                        'direccion_fiscal': '',
                        'rut': ''
                    }
                )

                SolicitudCliente.objects.update_or_create(
                    cliente=cliente,
                    defaults={'estado': 'aceptado'}
                )
        except Exception as e:
            logger.exception("Error al asignar rol o crear relación:")
            return Response({'error': 'Error al asociar usuario con su rol.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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

        except Exception:
            logger.exception("Error en LoginView:")
            return Response({'error': 'Error interno en el servidor.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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

            if usuario_actualizado.rol == 'tecnico':
                tecnico, _ = Tecnico.objects.get_or_create(usuario=usuario_actualizado)
                if obra:
                    obra.tecnico = tecnico
                    obra.save()

            elif usuario_actualizado.rol == 'supervisor':
                supervisor, created = SupervisorObra.objects.get_or_create(
                    usuario=usuario_actualizado,
                    defaults={'telefono': '', 'nivel_capacitacion': 'no_hay', 'obra': obra}
                )
                if not created and obra:
                    supervisor.obra = obra
                    supervisor.save()

            return Response({
                "mensaje": "Usuario actualizado correctamente.",
                "usuario": UsuarioSerializer(usuario_actualizado).data
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListarUsuarios(APIView):
    permission_classes = [RutaProtegida(['superadmin'])]

    def get(self, request):
        usuarios = Usuario.objects.all()
        serializer = UsuarioSerializer(usuarios, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
