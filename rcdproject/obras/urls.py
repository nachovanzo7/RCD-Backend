from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    DetallesObra,
    RegistroObra,
    ListarSolicitudesObra,
    AprobarSolicitudObra,
    RechazarSolicitudObra,
    ListarObrasAprobadas,
    ActualizarObra,
    EliminarObra,
    MarcarObraTerminada,
    ListarObraPorCliente,
    SupervisoresDeObra
)

urlpatterns = [
    path('registro/', RegistroObra.as_view(), name='registro-obra'),
    path('solicitudes/', ListarSolicitudesObra.as_view(), name='lista-solicitudes-obra'),
    path('solicitudes/<int:pk>/aprobar/', AprobarSolicitudObra.as_view(), name='aprobar-solicitud-obra'),
    path('solicitudes/<int:pk>/rechazar/', RechazarSolicitudObra.as_view(), name='rechazar-solicitud-obra'),
    path('solicitudes/<int:pk>/terminar/', MarcarObraTerminada.as_view(), name='terminar-solicitud-obra'),
    path('aprobadas/', ListarObrasAprobadas.as_view(), name='lista-obras-aprobadas'),
    path('<int:pk>/actualizar/', ActualizarObra.as_view(), name='actualizar-obra'),
    path('<int:pk>/eliminar/', EliminarObra.as_view(), name='eliminar-obra'),
    path('<int:pk>/', DetallesObra.as_view(), name='detalles-obra'),
    path('<int:pk>/supervisores/', SupervisoresDeObra.as_view(), name='supervisores-obra'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
