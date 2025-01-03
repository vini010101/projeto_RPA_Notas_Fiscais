from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm



def login_view(request):
    # Para requisições GET, exibe um formulário vazio
    form = AuthenticationForm()
    
    # Renderiza o template com o formulário
    return render(request, 'accounts/login.html', {'form': form})



def usuario_view(request):
    # Para requisições GET, exibe um formulário vazio
    form = UserCreationForm()

    # Renderiza o template com o formulário
    return render(request, 'accounts/criar_usuario.html', {'form': form})