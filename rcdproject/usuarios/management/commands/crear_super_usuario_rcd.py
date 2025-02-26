from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

Usuario = get_user_model()

class Command(BaseCommand):
    help = 'Crea el superusuario "RCD Gestion"'

    def handle(self, *args, **options):
        nombre_usuario = 'Gestion RCD'
        email = 'RCDgestion@gmail.com'
        contrasena = 'Añonuevovidanueva'
        rol = 'super_administrador'

        if not Usuario.objects.filter(username=nombre_usuario).exists():
            Usuario.objects.create_superuser(username=nombre_usuario, email=email, password=contrasena, rol=rol)
            self.stdout.write(self.style.SUCCESS('Superusuario "RCD Gestion" creado exitosamente.'))
        else:
            self.stdout.write(self.style.WARNING('El superusuario ya existe.'))
