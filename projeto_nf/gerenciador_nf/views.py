from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import NotaFiscal
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from .processar_nota import processar_nota_fiscal
import logging
from django.contrib.auth.decorators import login_required
from enviar_form import enviar_email
from django.http import JsonResponse
import os



# Função para renderizar a página principal
def pagina_principal(request):
    if request.method == 'GET':
        return render(request, 'accounts/index.html')



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
            return redirect('servicos')  # Redireciona para a página principal
        else:
            # Se não for encontrado ou a senha estiver errada
            messages.error(request, 'Credenciais inválidas. Tente novamente.')  # Mensagem de erro
            return redirect('login')  # Redireciona para a página de login com erro


def criar_usuario(request):
    if request.method == 'GET':
        return render(request, 'accounts/criar_usuario.html')

    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Verifica se o nome de usuário já existe no banco
        if User.objects.filter(username=username).exists():
            messages.error(request, "Usuário já existe. Escolha outro nome de usuário.")
            return render(request, 'accounts/criar_usuario.html')  # Retorna o formulário com a mensagem de erro
        
        try:
            # Cria o usuário utilizando o método create_user (que faz o hash da senha)
            user = User.objects.create_user(username=username, password=password)
            user.save()
            messages.success(request, 'Usuário criado com sucesso!')
            return redirect('login')  # Redireciona para uma página de sucesso ou para a lista de usuários
        except Exception as e:
            messages.error(request, f'Erro ao criar o usuário: {str(e)}')
            return render(request, 'accounts/criar_usuario.html')  # Retorna o formulário com a mensagem de erro



def pagina_orcamento(request):
    if request.method == 'GET':
        return render(request, 'accounts/orcamentos.html')
    
    if request.method == 'POST':
        # Obtém os dados do formulário
        nome = request.POST.get('nome')
        fone = request.POST.get('fone')
        fone2 = request.POST.get('fone2')
        email = request.POST.get('email')
        mensagem = request.POST.get('mensagem')
        tempo = request.POST.get('tempo')
        custo_estimado = request.POST.get('custo_estimado')
        fotos = request.FILES.getlist('fotos')

        # Diretório temporário para salvar os arquivos
        temp_dir = 'temp_uploads'
        os.makedirs(temp_dir, exist_ok=True)

        # Salva os arquivos temporariamente
        fotos_paths = []
        for foto in fotos:
            temp_path = os.path.join(temp_dir, foto.name)
            with open(temp_path, 'wb+') as destination:
                for chunk in foto.chunks():
                    destination.write(chunk)
            fotos_paths.append(temp_path)

        # Envia o e-mail
        try:
            enviar_email(nome, fone, fone2, email, mensagem, tempo, custo_estimado, fotos_paths)
            mensagem_status = "E-mail enviado com sucesso!"
        except Exception as e:
            mensagem_status = f"Erro ao enviar o e-mail: {e}"

        # Remove os arquivos temporários
        for foto_path in fotos_paths:
            try:
                os.remove(foto_path)
            except Exception as e:
                print(f"Erro ao excluir o arquivo {foto_path}: {e}")

        return render(request, 'accounts/orcamentos.html', {'mensagem_status': mensagem_status})




# Função para renderizar a página de escolha dos serviços
def pagina_servicos(request):
    if request.method == 'GET':
        return render(request, 'accounts/servicos.html')
    

    # Função para renderizar a página de consulta de notas e para fazer requisisoes para o banco de dados
@login_required
def consultar_notas(request):
    notas_fiscais = NotaFiscal.objects.all()
    
    if request.method == 'GET':
        return render(request, 'accounts/consultar_notas.html', {'notas_fiscais': notas_fiscais})
    

    # Função para renderizar a página de deletar Notas que não são mais necessarias
@login_required
def deletar_notas(request):
    notas_fiscais = NotaFiscal.objects.all()
    if request.method == 'GET':
        return render(request, 'accounts/deletar_notas.html', {'notas_fiscais': notas_fiscais})
    elif request.method == 'POST':
        nota_id = request.POST.get('nota_id')
        if nota_id:
            try:
                nota = NotaFiscal.objects.get(id=nota_id)
                nota.delete()
                return redirect('deletar_notas')
            except NotaFiscal.DoesNotExist:
                return render(request, 'accounts/deletar_notas.html', {
                    'notas_fiscais': NotaFiscal.objects.all(),
                    'error_message': 'Nota Fiscal não encontrada!'
                })

logger = logging.getLogger(__name__)

@login_required
def upload_notas(request):
    if request.method == "POST":
        cpf_cnpj = request.POST.get('CPF-CNPJ')
        valor_nota = request.POST.get('Valor-nota')
        data_nota = request.POST.get('data-nota')
        descricao_produto = request.POST.get('descricao-nota')
        arquivo = request.FILES.get('nota_fiscal')

        try:
            nota = NotaFiscal(
                usuario=request.user,  # Associa ao usuário autenticado
                cpf_cnpj=cpf_cnpj,
                valor_nota=valor_nota,
                data_nota=data_nota,
                descricao_produto=descricao_produto,
                arquivo=arquivo
            )
            nota.save()
            messages.success(request, "Nota Fiscal cadastrada com sucesso!")
        except Exception as e:
            messages.error(request, 'Erro ao cadastrar a nota fiscal:{str(e)}')
    
    return render(request, 'accounts/upload_notas.html')