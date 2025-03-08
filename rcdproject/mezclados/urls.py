from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import RegistrarMezclado, ListarMezclado, MezcladoDetalle


urlpatterns = [
    path('registrar/', RegistrarMezclado.as_view(), name='registrar-mezclado'),
    path('lista/', ListarMezclado.as_view(), name='lista-mezclados'),
    path('detalle/', MezcladoDetalle.as_view(), name='detalle-mezclado'),
]
