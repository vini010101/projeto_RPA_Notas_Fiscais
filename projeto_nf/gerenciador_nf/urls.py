from django.urls import path
from .views import login, criar_usuario, pagina_principal


urlpatterns = [
    path('', login, name='login'),  # Rota para login
    path('criar_usuario/', criar_usuario, name='criar_usuario'),  # Rota para criar usuário
    path('index/', pagina_principal, name='index'),  # Rota para a página inicial
]
