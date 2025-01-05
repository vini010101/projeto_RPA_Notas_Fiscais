from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages

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
