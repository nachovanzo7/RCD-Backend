from django.urls import path
from .views import (
    RegistroCliente,
    ListarSolicitudesCliente,
    AprobarSolicitudCliente,
    RechazarSolicitudCliente,
    ListarClientesAprobados, 
    ActualizarCliente
)

urlpatterns = [
    path('registro/', RegistroCliente.as_view(), name='registro-cliente'),
    path('solicitudes/', ListarSolicitudesCliente.as_view(), name='lista-solicitudes'),
    path('solicitudes/<int:pk>/aprobar/', AprobarSolicitudCliente.as_view(), name='aprobar-solicitud'),
    path('solicitudes/<int:pk>/rechazar/', RechazarSolicitudCliente.as_view(), name='rechazar-solicitud'),
    path('aprobados/', ListarClientesAprobados.as_view(), name='lista-clientes-aprobados'),
    path('clientes/<int:pk>/actualizar/', ActualizarCliente.as_view(), name='actualizar-cliente'),
]
