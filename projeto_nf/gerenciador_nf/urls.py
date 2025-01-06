from django.urls import path
from .views import login, criar_usuario, pagina_principal, consultar_notas, deletar_notas, upload_notas


urlpatterns = [
    path('', login, name='login'),  # Rota para login
    path('criar_usuario/', criar_usuario, name='criar_usuario'),  # Rota para criar usuário
    path('index/', pagina_principal, name='index'),  # Rota para a página inicial
    path('consultar_notas/', consultar_notas, name='consultar_notas'),  # Rota para a página de consulta de notas
    path('deletar_notas/', deletar_notas, name='deletar_notas'),  # Rota para a página que deleta alguma nota
    path('upload_notas/', upload_notas, name='upload_notas'),  # Rota para a página de Upload de notas notas no banco de dados
]
