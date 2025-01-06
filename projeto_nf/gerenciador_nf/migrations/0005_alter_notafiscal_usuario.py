# Generated by Django 4.2.15 on 2025-01-06 17:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('gerenciador_nf', '0004_remove_usuarios_password_usuarios_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notafiscal',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
