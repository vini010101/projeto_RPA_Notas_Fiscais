# Generated by Django 4.2.15 on 2025-01-07 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gerenciador_nf', '0005_alter_notafiscal_usuario'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notafiscal',
            name='criado_em',
        ),
        migrations.AddField(
            model_name='notafiscal',
            name='arquivo',
            field=models.FileField(default='uploads/default.txt', upload_to='notas_fiscais/'),
        ),
        migrations.AlterField(
            model_name='notafiscal',
            name='cpf_cnpj',
            field=models.CharField(max_length=20),
        ),
    ]
