from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from gerenciador_nf.models import NotaFiscal, UploadNotaFiscal
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from .processar_nota import processar_nota_fiscal

# Função para criar um novo usuário
def criar_usuario(request):
    if request.method == 'GET':
        return render(request, 'accounts/criar_usuario.html')
    
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Verifica se o nome de usuário já existe no banco
        if User.objects.filter(username=username).exists():
            return HttpResponse("Usuário já existe. Escolha outro nome de usuário.", status=400)
        
        try:
            # Cria o usuário utilizando o método create_user (que faz o hash da senha)
            user = User.objects.create_user(username=username, password=password)
            user.save()
            return HttpResponse("Usuário criado com sucesso!", status=201)
        except Exception as e:
            return HttpResponse(f"Erro ao criar o usuário: {str(e)}", status=500)


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
    

def upload_notas(request):
    if request.method == 'POST' and request.FILES.get('nota_fiscal'):
        arquivo = request.FILES['nota_fiscal']
        
        # Processar o arquivo de nota fiscal
        dados_nota = processar_nota_fiscal(arquivo)

        # Verificar se todos os campos foram extraídos corretamente
        if dados_nota['cpf_cnpj'] and dados_nota['data_nota'] and dados_nota['valor_nota'] and dados_nota['descricao_produto']:
            # Criar uma nova Nota Fiscal no banco de dados
            nota_fiscal = NotaFiscal.objects.create(
                cpf_cnpj=dados_nota['cpf_cnpj'],
                valor_nota=dados_nota['valor_nota'],
                data_nota=dados_nota['data_nota'],
                descricao_produto=dados_nota['descricao_produto'],
                usuario=request.user
            )
            
            # Criar o upload da nota fiscal no banco de dados
            UploadNotaFiscal.objects.create(
                nota_fiscal=nota_fiscal,
                caminho_arquivo=arquivo.name
            )
            
            # Redirecionar para uma página de sucesso
            return HttpResponse(f"arquivo enviado com sucesso", status=200)

    # Renderiza a página de upload para GET ou se não houver arquivo
    return render(request, 'accounts/upload_notas.html')