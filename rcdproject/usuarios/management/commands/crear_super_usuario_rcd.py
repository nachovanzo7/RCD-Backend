from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

Usuario = get_user_model()

class Command(BaseCommand):
    help = 'Crea el superusuario "RCD Gestion"'

    def handle(self, *args, **options):
        email = 'RCDgestion@gmail.com'
        password = 'Añonuevovidanueva'
        rol = 'superadmin'  # ajusta el nombre del rol que usas

        if not Usuario.objects.filter(email=email).exists():
            Usuario.objects.create_superuser(email=email, password=password, rol=rol)
            self.stdout.write(self.style.SUCCESS('Superusuario creado exitosamente.'))
        else:
            self.stdout.write(self.style.WARNING('El superusuario ya existe.'))
