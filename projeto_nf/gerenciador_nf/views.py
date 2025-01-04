from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import Usuarios
from django.contrib import messages





class LoginView(FormView):
    template_name = 'accounts/login.html'  # Template de login
    form_class = AuthenticationForm  # Formulário de autenticação
    success_url = reverse_lazy('index')  # URL de redirecionamento após login bem-sucedido

    def form_valid(self, form):
        # Obter os dados do formulário
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        
        # Buscar no banco de dados pelo usuário e senha
        try:
            usuario = Usuarios.objects.get(nome_usuario=username)
            if usuario.senha == password:  # Comparando a senha
                # Realiza o login do usuário manualmente (não usando authenticate)
                self.request.session['usuario_id'] = usuario.id  # Você pode armazenar o ID do usuário na sessão
                return redirect(self.success_url)  # Redireciona para a página de sucesso
            else:
                form.add_error(None, "Usuário ou senha incorretos.")  # Se a senha não bater
        except Usuarios.DoesNotExist:
            form.add_error(None, "Usuário ou senha incorretos.")  # Se o usuário não existir

        return self.form_invalid(form)  # Retorna ao formulário com erro

    def form_invalid(self, form):
        # Exibe o formulário com os erros
        return render(self.request, self.template_name, {'form': form})





class CriarUsuarioView(FormView):
    template_name = 'accounts/criar_usuario.html'  # Template de criação de usuário
    form_class = UserCreationForm  # Formulário para criação de usuários
    success_url = reverse_lazy('login')  # URL de redirecionamento após criação bem-sucedida

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            # O método `save()` já lida com a senha e a cria de forma segura
            form.save()  # Salva o novo usuário no banco de dados
            
            messages.success(request, "Conta criada com sucesso! Faça login.")  # Mensagem de sucesso
            return self.form_valid(form)  # Redireciona para o success_url
        else:
            messages.error(request, "Erro ao criar conta. Verifique os dados.")  # Mensagem de erro
            return self.form_invalid(form)  # Renderiza novamente o formulário
        
    
class PaginaPrincipalView(FormView):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
