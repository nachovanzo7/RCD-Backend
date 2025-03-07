from django.urls import path
from .views import CrearSupervisorObra, ListarSupervisoresObra, ModificarDatosSupervisorObra, EliminarSupervisorObra

urlpatterns = [
    path('registro/', CrearSupervisorObra.as_view(), name='registro-supervisor-obra'),
    path(
    '<int:obra_id>/supervisores/', 
    ListarSupervisoresObra.as_view(), 
    name='supervisores-obra'
),
    path('modificar/<int:pk>/', ModificarDatosSupervisorObra.as_view(), name='modificar-supervisor-obra'),
    path('eliminar/<int:pk>/', EliminarSupervisorObra.as_view(), name='eliminar-supervisor-obra'),
]
