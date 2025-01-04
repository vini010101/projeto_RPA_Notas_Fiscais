from . import views
from django.urls import path
from .views import LoginView, CriarUsuarioView, PaginaPrincipalView




urlpatterns = [
    path('', LoginView.as_view(), name='login'),  # Rota para login
    path('criar_usuario/', CriarUsuarioView.as_view(), name='criar_usuario'),  # Rota para criar usuário
    path('index/', PaginaPrincipalView.as_view(), name='index'),  # Rota para a página inicial
]