from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import NotaFiscal, UploadNotaFiscal
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from .processar_nota import processar_nota_fiscal
import logging

# Função para criar um novo usuário
def criar_usuario(request):
    if request.method == 'GET':
        return render(request, 'accounts/criar_usuario.html')
    
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Verifica se o nome de usuário já existe no banco
        if User.objects.filter(username=username).exists():
            return messages.error("Usuário já existe. Escolha outro nome de usuário.")
        
        try:
            # Cria o usuário utilizando o método create_user (que faz o hash da senha)
            user = User.objects.create_user(username=username, password=password)
            user.save()
            return messages.success(f"Usuario criado com sucesso")
        except Exception as e:
            return messages.error(f"Erro ao criar o usuário, Tente Novamente mais tarde")


# Função para realizar o login do usuário
def login(request):
    if request.method == 'GET':
        return render(request, 'accounts/login.html')
    
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Tenta autenticar o usuário
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Se o usuário for autenticado e estiver ativo, faz login
            auth_login(request, user)
            return redirect('index')  # Redireciona para a página principal
        else:
            # Se não for encontrado ou a senha estiver errada
            messages.error(request, 'Credenciais inválidas. Tente novamente.')  # Mensagem de erro
            return redirect('login')  # Redireciona para a página de login com erro


# Função para renderizar a página principal
def pagina_principal(request):
    if request.method == 'GET':
        return render(request, 'accounts/index.html')
    

    # Função para renderizar a página de consulta de notas e para fazer requisisoes para o banco de dados
def consultar_notas(request):
    if request.method == 'GET':
        return render(request, 'accounts/consultar_notas.html')
    

    # Função para renderizar a página de deletar Notas que não são mais necessarias
def deletar_notas(request):
    if request.method == 'GET':
        return render(request, 'accounts/deletar_notas.html')
    

logger = logging.getLogger(__name__)

def upload_notas(request):
    if request.method == 'POST':
        # Caso o usuário tenha preenchido os dados manualmente
        cpf_cnpj = request.POST.get('CPF_CNPJ')
        valor_nota = request.POST.get('valor_nota')
        data_nota = request.POST.get('data_nota')
        descricao_produto = request.POST.get('descricao_produto')

        # Caso o usuário tenha feito o upload do arquivo
        arquivo = request.FILES.get('nota_fiscal')

        if arquivo:
            logger.debug(f"Arquivo de nota fiscal recebido: {arquivo.name}")
            # Processamento do arquivo pode ser feito aqui (se necessário)
            # Lembre-se de que você pode processar o arquivo e extrair os dados automaticamente mais tarde, se necessário.

        # Verificar se os dados manuais foram preenchidos
        if cpf_cnpj and valor_nota and data_nota and descricao_produto:
            try:
                # Criar uma nova Nota Fiscal no banco de dados com os dados manuais
                nota_fiscal = NotaFiscal.objects.create(
                    cpf_cnpj=cpf_cnpj,
                    valor_nota=valor_nota,
                    data_nota=data_nota,
                    descricao_produto=descricao_produto,
                    usuario=request.user  # Associando o usuário ao objeto
                )
                logger.debug(f"Nota fiscal criada com sucesso: {nota_fiscal}")

                # Criar o upload da nota fiscal no banco de dados, se houver um arquivo
                if arquivo:
                    UploadNotaFiscal.objects.create(
                        nota_fiscal=nota_fiscal,
                        caminho_arquivo=arquivo.name
                    )
                    logger.debug(f"Upload da nota fiscal criado com sucesso")

                return HttpResponse("Dados da nota fiscal cadastrados com sucesso", status=200)
            
            except Exception as e:
                logger.error(f"Erro ao criar nota fiscal no banco: {str(e)}")
                return HttpResponse(f"Erro ao criar nota fiscal: {str(e)}", status=500)
        
        else:
            return HttpResponse("Dados incompletos. Por favor, preencha todos os campos necessários.", status=400)

    # Caso o método não seja POST, renderizar o formulário
    return render(request, 'accounts/upload_notas.html')