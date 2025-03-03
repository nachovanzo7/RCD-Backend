from django.urls import path
from .views import CrearPuntoLimpio, ListarPuntosLimpios, ActualizarPuntoLimpio, PuntoLimpioDetalle

urlpatterns = [
    path('registro/', CrearPuntoLimpio.as_view(), name='registro-punto-limpio'),
    path('lista/', ListarPuntosLimpios.as_view(), name='lista-puntos-limpios'),
    path('<int:pk>/actualizar/', ActualizarPuntoLimpio.as_view(), name='actualizar-punto-limpio'),
    path('detalle/', PuntoLimpioDetalle.as_view(), name='detalle-punto-limpio'),
]

