from django.urls import path
from .views import login, criar_usuario, pagina_servicos, consultar_notas, deletar_notas, upload_notas, pagina_principal, pagina_orcamento


urlpatterns = [
    path('', pagina_principal, name='index'),  # Rota para login
    path('orcamento/', pagina_orcamento, name='orcamento'),  # Rota para a pagina de orçamento
    path('login/', login, name='login'),  # Rota para login
    path('criar_usuario/', criar_usuario, name='criar_usuario'),  # Rota para criar usuário
    path('servicos/', pagina_servicos, name='servicos'),  # Rota para a página de serviços
    path('consultar_notas/', consultar_notas, name='consultar_notas'),  # Rota para a página de consulta de notas
    path('deletar_notas/', deletar_notas, name='deletar_notas'),  # Rota para a página que deleta alguma nota
    path('upload_notas/', upload_notas, name='upload_notas'),  # Rota para a página de Upload de notas notas no banco de dados
]
