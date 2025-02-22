from django.urls import path
from .views import CrearCoordinacionRetiro, ListarCoordinacionesRetiro, AceptarCoordinacionRetiro, RechazarCoordinacionRetiro, ListarSolicitudesAceptadasCoordinacion

urlpatterns = [
    path('registro/', CrearCoordinacionRetiro.as_view(), name='registro-coordinacion'),
    path('lista/', ListarCoordinacionesRetiro.as_view(), name='lista-coordinaciones'),
    path('<int:pk>/aceptar/', AceptarCoordinacionRetiro.as_view(), name='actualizar-coordinacion'),
    path('<int:pk>/rechazar/', RechazarCoordinacionRetiro.as_view(), name='rechazar-coordinacion'),
    path('aceptadas/', ListarSolicitudesAceptadasCoordinacion.as_view(), name='lista-coordinaciones-aceptadas'),
]
