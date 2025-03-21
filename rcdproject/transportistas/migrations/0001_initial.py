# Generated by Django 5.1.5 on 2025-02-09 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Transportista',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200)),
                ('contacto', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('tipo_vehiculo', models.CharField(max_length=100)),
                ('tipo_material', models.CharField(choices=[('escombro_limpio', 'Escombro Limpio'), ('plastico', 'Plástico'), ('papel_carton', 'Papel y Carton'), ('metales', 'Metales'), ('madera', 'Madera'), ('mezclados', 'Mezclados'), ('peligrosos', 'Peligrosos')], max_length=20)),
            ],
        ),
    ]
