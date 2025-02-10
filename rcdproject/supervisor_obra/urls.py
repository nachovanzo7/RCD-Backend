from django.urls import path
from .views import CrearSupervisorObra, ListarSupervisoresObra

urlpatterns = [
    path('registro/', CrearSupervisorObra.as_view(), name='registro-supervisor-obra'),
    path('lista/', ListarSupervisoresObra.as_view(), name='lista-supervisores-obra'),
]
