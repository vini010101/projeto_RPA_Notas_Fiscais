from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, User
from django.db import models
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from django.db.models.signals import post_save
from django.dispatch import receiver


class UsuarioManager(BaseUserManager):
    def ativo(self):
        return self.filter(ativo=True)

    def buscar_por_nome(self, nome_usuario):
        return self.filter(nome_usuario=nome_usuario)

    def criar_usuario(self, user, nome_usuario=None, senha=None):
        """Método para criar um novo usuário associado ao User padrão do Django."""
        senha_criptografada = make_password(senha)
        usuario = self.create(
            user=user,
            nome_usuario=nome_usuario or user.username,
            senha=senha_criptografada
        )
        return usuario


class Usuarios(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    nome_usuario = models.CharField(max_length=100, unique=True)
    senha = models.CharField(max_length=100)
    data_criacao = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(default=timezone.now)
    ativo = models.BooleanField(default=True)

    objects = UsuarioManager()

    def __str__(self):
        return self.nome_usuario

    # Sobrescrever o método save para garantir a sincronização
    def save(self, *args, **kwargs):
        # Sincronizar alterações do modelo User
        if self.user:
            self.nome_usuario = self.user.username
            self.senha = self.user.password
            self.last_login = self.user.last_login
            self.ativo = self.user.is_active
        super(Usuarios, self).save(*args, **kwargs)


# Usando sinal para sincronizar os dados após salvar um usuário
@receiver(post_save, sender=User)
def sincronizar_usuario(sender, instance, created, **kwargs):
    """
    Sincroniza as alterações no modelo `User` com o modelo `Usuarios`.
    Cria um objeto `Usuarios` se for um novo usuário.
    """
    if created:
        Usuarios.objects.create(user=instance)
    else:
        # Atualiza os campos correspondentes
        usuario, _ = Usuarios.objects.get_or_create(user=instance)
        usuario.save()


class NotaFiscal(models.Model):
    cpf_cnpj = models.CharField(max_length=18)
    valor_nota = models.DecimalField(max_digits=10, decimal_places=2)
    data_nota = models.DateField()
    descricao_produto = models.TextField()
    criado_em = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Nota Fiscal - {self.cpf_cnpj} - {self.valor_nota} - {self.data_nota}"


class UploadNotaFiscal(models.Model):
    id = models.AutoField(primary_key=True)
    nota_fiscal = models.ForeignKey(NotaFiscal, on_delete=models.CASCADE, related_name="uploads")
    caminho_arquivo = models.CharField(max_length=255)
    data_upload = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Upload - {self.nota_fiscal.cpf_cnpj} - {self.data_upload}"
