from django.db import models

# Modelo de Usuário
class Usuarios(models.Model):
    id = models.AutoField(primary_key=True)
    nome_usuario = models.CharField(max_length=100)
    senha = models.CharField(max_length=100)
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome_usuario


# Modelo de Nota Fiscal
class NotaFiscal(models.Model):
    cpf_cnpj = models.CharField(max_length=18)
    valor_nota = models.DecimalField(max_digits=10, decimal_places=2)
    data_nota = models.DateField()
    descricao_produto = models.TextField()
    criado_em = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE)

    def __str__(self):
        return f"Nota Fiscal - {self.cpf_cnpj} - {self.valor_nota} - {self.data_nota}"


# Modelo de Upload de Nota Fiscal
class UploadNotaFiscal(models.Model):
    id = models.AutoField(primary_key=True)
    nota_fiscal = models.ForeignKey(NotaFiscal, on_delete=models.CASCADE, related_name="uploads")
    caminho_arquivo = models.CharField(max_length=255)
    data_upload = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Upload - {self.nota_fiscal.cpf_cnpj} - {self.data_upload}"