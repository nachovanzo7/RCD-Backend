from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/clientes/', include('clientes.urls')),
    path('api/obras/', include('obras.urls')),
    path('api/transportistas/', include('transportistas.urls')),
    path('api/empresas/', include('empresas_gestoras.urls')),
    path('api/supervisores/', include('supervisor_obra.urls')),
    path('api/puntolimpio/', include('puntolimpio.urls')),
    path('api/materiales/', include('materiales.urls')),
    path('api/visitas/', include('visitas.urls')),
    path('api/tecnicos/', include('tecnicos.urls')),
    path('api/coordinacionretiro/', include('coordinacionretiro.urls')),
    path('api/capacitaciones/', include('capacitacion.urls')),
    path('api/formularios/', include('formularios.urls')),
    path('api/notificaciones/', include('notificaciones.urls')),
    path('api/usuarios/', include('usuarios.urls')),
    path('api/mezclados/', include('mezclados.urls')),
    path('api/fotos/', include('fotos.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
