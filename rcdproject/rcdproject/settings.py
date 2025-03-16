import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# SECRET_KEY: asegúrate de definirla en producción (puedes agregarla en tu .env)
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-d&@!3$x18jknwgos(acz6+&2_)-*+wsv85(j)e&fg&l)czvg8v')

# DEBUG: se activa solo si la variable de entorno lo indica
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

# ALLOWED_HOSTS: se define a partir de la variable de entorno
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '*').split(',')

INSTALLED_APPS = [
    'corsheaders',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rcdproject.usuarios.apps.UsuariosConfig',
    'rest_framework.authtoken',
    'rcdproject.clientes.apps.ClientesConfig',
    'rcdproject.transportistas.apps.TransportistasConfig',
    'rcdproject.empresas_gestoras.apps.EmpresasGestorasConfig',
    'rest_framework',
    'rcdproject.supervisor_obra.apps.SupervisorObraConfig',
    'rcdproject.obras.apps.ObrasConfig',
    'rcdproject.mezclados.apps.MezcladosConfig',
    'rcdproject.tecnicos.apps.TecnicosConfig',
    'rcdproject.visitas.apps.VisitasConfig',
    'rcdproject.fotos.apps.FotosConfig',
    'rcdproject.formularios.apps.FormulariosConfig',
    'rcdproject.capacitacion.apps.CapacitacionConfig',
    'rcdproject.condiciondeobras.apps.CondiciondeobrasConfig',
    'rcdproject.coordinacionretiro.apps.CoordinacionretiroConfig',
    'rcdproject.puntolimpio.apps.PuntolimpioConfig',
    'rcdproject.materiales.apps.MaterialesConfig',
    'rcdproject.notificaciones.apps.NotificacionesConfig',
]

# Usamos el app_label corto definido en UsuariosConfig (label = 'rcdproject_usuarios')
AUTH_USER_MODEL = 'rcdproject_usuarios.Usuario'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ALLOWED_ORIGINS = [
    'http://localhost:5173',
    "https://rcd-frontend.onrender.com",
]

ROOT_URLCONF = 'rcdproject.rcdproject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'rcdproject.rcdproject.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB', 'gestion_rcd_database'),
        'USER': os.environ.get('POSTGRES_USER', 'rcd_username'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', 'rcd_gestion'),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('POSTGRES_PORT', '5432'),
        'OPTIONS': {
            'client_encoding': 'UTF8',
        }
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
