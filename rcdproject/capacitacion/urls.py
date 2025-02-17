from django.urls import path
from .views import CrearCapacitacion, ListarCapacitaciones

urlpatterns = [
    path('registro/', CrearCapacitacion.as_view(), name='registro-capacitacion'),
    path('lista/', ListarCapacitaciones.as_view(), name='lista-capacitaciones'),
]
