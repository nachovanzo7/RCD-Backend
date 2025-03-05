from django.urls import path
from .views import (
    CrearCoordinacionRetiro, 
    ListarCoordinacionesRetiro, 
    AceptarCoordinacionRetiro, 
    RechazarCoordinacionRetiro, 
    ListarSolicitudesAceptadasCoordinacion,
    DetallesCoordinacion,
    ActualizarCoordinacionRetiro
)

urlpatterns = [
    path('registro/', CrearCoordinacionRetiro.as_view(), name='registro-coordinacion'),
    path('lista/', ListarCoordinacionesRetiro.as_view(), name='lista-coordinaciones'),
    path('<int:pk>/aceptar/', AceptarCoordinacionRetiro.as_view(), name='actualizar-coordinacion'),
    path('<int:pk>/rechazar/', RechazarCoordinacionRetiro.as_view(), name='rechazar-coordinacion'),
    path('aceptadas/', ListarSolicitudesAceptadasCoordinacion.as_view(), name='lista-coordinaciones-aceptadas'),
    path('<int:pk>/', DetallesCoordinacion.as_view(), name='detalle-coordinacion'),
    path('<int:pk>/actualizar/', ActualizarCoordinacionRetiro.as_view(), name='actualizar-coordinacion'),
]
