from django.urls import path
from .views import ImovelListCreateAPIView, ImovelDetailAPIView,UsuarioAPIView, ImagemImovelListCreateAPIView, MensagemAPIView
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('mensagens/', MensagemAPIView.as_view(), name='mensagens'),
    path('imagens/', ImagemImovelListCreateAPIView.as_view(), name='imagens-list-create'),
    path('imoveis/', ImovelListCreateAPIView.as_view(), name='imovel-list-create'),
    path('imoveis/<int:pk>/', ImovelDetailAPIView.as_view(), name='imovel-detail'),
    path('usuarios/', UsuarioAPIView.as_view(), name='usuarios'),
    path('token/', obtain_auth_token, name='api_token_auth'),
]
