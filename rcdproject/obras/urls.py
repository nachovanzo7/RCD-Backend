from django.urls import path
from .views import (
    RegistroObra,
    ListarSolicitudesObra,
    AprobarSolicitudObra,
    RechazarSolicitudObra,
    ListarObrasAprobadas,
    ModificarDatosObra
)

urlpatterns = [
    path('registro/', RegistroObra.as_view(), name='registro-obra'),
    path('solicitudes/', ListarSolicitudesObra.as_view(), name='lista-solicitudes-obra'),
    path('solicitudes/<int:pk>/aprobar/', AprobarSolicitudObra.as_view(), name='aprobar-solicitud-obra'),
    path('solicitudes/<int:pk>/rechazar/', RechazarSolicitudObra.as_view(), name='rechazar-solicitud-obra'),
    path('aprobadas/', ListarObrasAprobadas.as_view(), name='lista-obras-aprobadas'),
    path('<int:pk>/actualizar/', ModificarDatosObra.as_view, name='actualizar-obras'),
]
