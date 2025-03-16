from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/clientes/', include('rcdproject.clientes.urls')),
    path('api/obras/', include('rcdproject.obras.urls')),
    path('api/transportistas/', include('rcdproject.transportistas.urls')),
    path('api/empresas/', include('rcdproject.empresas_gestoras.urls')),
    path('api/supervisores/', include('rcdproject.supervisor_obra.urls')),
    path('api/puntolimpio/', include('rcdproject.puntolimpio.urls')),
    path('api/materiales/', include('rcdproject.materiales.urls')),
    path('api/visitas/', include('rcdproject.visitas.urls')),
    path('api/tecnicos/', include('rcdproject.tecnicos.urls')),
    path('api/coordinacionretiro/', include('rcdproject.coordinacionretiro.urls')),
    path('api/capacitaciones/', include('rcdproject.capacitacion.urls')),
    path('api/formularios/', include('rcdproject.formularios.urls')),
    path('api/notificaciones/', include('rcdproject.notificaciones.urls')),
    path('api/usuarios/', include('rcdproject.usuarios.urls')),
    path('api/mezclados/', include('rcdproject.mezclados.urls')),
    path('api/fotos/', include('rcdproject.fotos.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
