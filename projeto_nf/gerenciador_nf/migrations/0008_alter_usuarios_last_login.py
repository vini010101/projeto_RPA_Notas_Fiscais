# Generated by Django 4.2.15 on 2025-01-07 21:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gerenciador_nf', '0007_alter_notafiscal_cpf_cnpj'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuarios',
            name='last_login',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
