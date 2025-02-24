from django.urls import path
from .views import ActualizarDatosSuperUsuario, CrearUsuario

urlpatterns = [
    path('actualizar-datos-super-admin/', ActualizarDatosSuperUsuario.as_view(), name='actualizar_datos_superusuario'),
    path('super-admin-crear-usuario/', CrearUsuario.as_view(), name='crear_usuario'),
]
