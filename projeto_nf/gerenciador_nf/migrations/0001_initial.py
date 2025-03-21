# Generated by Django 4.2.15 on 2025-01-05 04:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='NotaFiscal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cpf_cnpj', models.CharField(max_length=18)),
                ('valor_nota', models.DecimalField(decimal_places=2, max_digits=10)),
                ('data_nota', models.DateField()),
                ('descricao_produto', models.TextField()),
                ('criado_em', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Usuarios',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nome_usuario', models.CharField(max_length=100)),
                ('senha', models.CharField(max_length=100)),
                ('data_criacao', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='UploadNotaFiscal',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('caminho_arquivo', models.CharField(max_length=255)),
                ('data_upload', models.DateTimeField(auto_now_add=True)),
                ('nota_fiscal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='uploads', to='gerenciador_nf.notafiscal')),
            ],
        ),
        migrations.AddField(
            model_name='notafiscal',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gerenciador_nf.usuarios'),
        ),
    ]
