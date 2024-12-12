# Generated by Django 5.0.7 on 2024-08-14 22:54

import django.db.models.manager
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UsuarioAcceso',
            fields=[
                ('cve_persona', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('login', models.CharField(max_length=10, unique=True, verbose_name='Nombre de usuario')),
                ('password', models.CharField(max_length=128)),
                ('activo', models.BooleanField(default=False)),
                ('email', models.EmailField(blank=True, max_length=254, null=True, unique=True)),
                ('staff', models.BooleanField(default=False)),
                ('superuser', models.BooleanField(default=False)),
                ('last_login', models.DateTimeField(blank=True, editable=False, null=True)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('avatar', models.ImageField(blank=True, default='avatar/default.png', null=True, upload_to='avatar')),
            ],
            options={
                'verbose_name': 'Acceso Usuario',
                'verbose_name_plural': 'Acceso Usuarios',
                'db_table': 'sistema_usuario',
                'managed': False,
            },
            managers=[
                ('object', django.db.models.manager.Manager()),
            ],
        ),
    ]
