# Generated by Django 4.2.15 on 2025-01-06 16:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('gerenciador_nf', '0003_usuarios_last_login_usuarios_password'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usuarios',
            name='password',
        ),
        migrations.AddField(
            model_name='usuarios',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='usuarios',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]