from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm



def login_view(request):
    if request.method == 'POST':
        # Inicializa o formulário com os dados enviados
        form = AuthenticationForm(request, data=request.POST)
        
        if form.is_valid():
            # Obtém os dados do formulário
            nome_usuario = form.cleaned_data.get('username')
            senha = form.cleaned_data.get('password')
            
            # Autentica o usuário
            usuario = authenticate(username=nome_usuario, password=senha)
            
            if usuario is not None:
                # Loga o usuário no sistema
                login(request, usuario)
                
                # Redireciona para a página index.html
                return redirect('index')
        else:
            # Se os dados forem inválidos, exibe o formulário com erros
            return render(request, 'accounts/login.html', {'form': form})
    else:
        # Para requisições GET, exibe um formulário vazio
        form = AuthenticationForm()
    
    return render(request, 'accounts/login.html', {'form': form})

def usuario_view(request):
    if request.method == 'POST':
        # Inicializa o formulário com os dados enviados
        form = UserCreationForm(request.POST)
        
        if form.is_valid():
            # Cria o novo usuário
            form.save()
            # Redireciona para uma página de sucesso ou login
            return redirect('login')  # Você pode ajustar a URL para o que desejar
    else:
        # Para requisições GET, exibe um formulário vazio
        form = UserCreationForm()

    # Renderiza o template com o formulário
    return render(request, 'accounts/criar_usuario.html', {'form': form})