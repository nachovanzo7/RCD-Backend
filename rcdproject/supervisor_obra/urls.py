from django.urls import path
from .views import CrearSupervisorObra, ListarSupervisoresObra, ModificarDatosSupervisorObra

urlpatterns = [
    path('registro/', CrearSupervisorObra.as_view(), name='registro-supervisor-obra'),
    path('lista/', ListarSupervisoresObra.as_view(), name='lista-supervisores-obra'),
    path('modificar/<int:pk>/', ModificarDatosSupervisorObra.as_view(), name='modificar-supervisor-obra'),
]
