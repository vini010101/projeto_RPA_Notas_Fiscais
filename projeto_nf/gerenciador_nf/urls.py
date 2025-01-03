from . import views
from django.urls import path




urlpatterns = [
    path('', views.login_view, name='login'),
    path('criar_usuario/', views.usuario_view, name='criar_usuario')
]