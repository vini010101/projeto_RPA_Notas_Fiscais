from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils import timezone
from django.contrib.auth.hashers import make_password

class UsuarioManager(BaseUserManager):
    def ativo(self):
        return self.filter(ativo=True)

    def buscar_por_nome(self, nome_usuario):
        return self.filter(nome_usuario=nome_usuario)

    def criar_usuario(self, nome_usuario, senha):
        """Método para criar um novo usuário com senha criptografada."""
        senha_criptografada = make_password(senha)
        usuario = self.create(
            nome_usuario=nome_usuario,
            senha=senha_criptografada
        )
        return usuario

class Usuarios(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    nome_usuario = models.CharField(max_length=100, unique=True)
    senha = models.CharField(max_length=100)
    data_criacao = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(default=timezone.now)
    ativo = models.BooleanField(default=True)

    objects = UsuarioManager()

    USERNAME_FIELD = 'nome_usuario'
    REQUIRED_FIELDS = ['senha']

    def __str__(self):
        return self.nome_usuario



class NotaFiscal(models.Model):
    cpf_cnpj = models.CharField(max_length=18)
    valor_nota = models.DecimalField(max_digits=10, decimal_places=2)
    data_nota = models.DateField()
    descricao_produto = models.TextField()
    criado_em = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE)

    def __str__(self):
        return f"Nota Fiscal - {self.cpf_cnpj} - {self.valor_nota} - {self.data_nota}"



class UploadNotaFiscal(models.Model):
    id = models.AutoField(primary_key=True)
    nota_fiscal = models.ForeignKey(NotaFiscal, on_delete=models.CASCADE, related_name="uploads")
    caminho_arquivo = models.CharField(max_length=255)
    data_upload = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Upload - {self.nota_fiscal.cpf_cnpj} - {self.data_upload}"