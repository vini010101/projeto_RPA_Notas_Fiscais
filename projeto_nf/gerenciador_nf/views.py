from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.utils.http import is_safe_url

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            nome_usuario = form.cleaned_data.get('username')
            senha = form.cleaned_data.get('password')
            usuario = authenticate(username=nome_usuario, password=senha)
            
            if usuario is not None:
                login(request, usuario)
                messages.success(request, 'Login realizado com sucesso!')
                
                # Redireciona para a página desejada ou para a página inicial
                redirect_url = request.GET.get('next', 'index')
                if is_safe_url(redirect_url, allowed_hosts=request.get_host()):
                    return redirect(redirect_url)
                return redirect('index')
            else:
                messages.error(request, 'Nome de usuário ou senha incorretos.')
        else:
            messages.error(request, 'Erro ao validar o formulário.')

    else:
        form = AuthenticationForm()
    
    context = {'form': form}
    return render(request, 'accounts/login.html', context)