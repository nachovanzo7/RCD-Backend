from django.urls import path
from .views import (
    RegistroCliente,
    ListarSolicitudesCliente,
    AprobarSolicitudCliente,
    RechazarSolicitudCliente,
    MarcarComoTerminadoSolicitudCliente,
    ListarClientesAprobados, 
    ActualizarCliente,
    DetalleCliente,
    EliminarCliente,
    ListarObraPorCliente,
    ListarPuntoLimpioPorCliente
)

urlpatterns = [
    path('registro/', RegistroCliente.as_view(), name='registro-cliente'),
    path('solicitudes/', ListarSolicitudesCliente.as_view(), name='lista-solicitudes'),
    path('solicitudes/<int:pk>/aprobar/', AprobarSolicitudCliente.as_view(), name='aprobar-solicitud'),
    path('solicitudes/<int:pk>/rechazar/', RechazarSolicitudCliente.as_view(), name='rechazar-solicitud'),
    path('solicitudes/<int:pk>/terminar/', MarcarComoTerminadoSolicitudCliente.as_view(), name='terminar-solicitud'),
    path('aprobados/', ListarClientesAprobados.as_view(), name='lista-clientes-aprobados'),
    path('<int:pk>/actualizar/', ActualizarCliente.as_view(), name='actualizar-cliente'),
    path('<int:pk>/', DetalleCliente.as_view(), name='obtener-cliente'),
    path('<int:pk>/eliminar/', EliminarCliente.as_view(), name='eliminar-cliente'),
    path('obras/', ListarObraPorCliente.as_view(), name='listar-obra-por-cliente'),
    path('puntos-limpios/', ListarPuntoLimpioPorCliente.as_view(), name='cliente-puntos-limpios'),

]
