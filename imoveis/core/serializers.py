from rest_framework import serializers
from django.contrib.auth import get_user_model
from core.models import Imovel, ImagemImovel, Mensagem
Usuario = get_user_model()

class ImovelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Imovel
        fields = '__all__'  # Inclui todos os campos do modelo

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'email', 'foto_perfil', 'telefone', 'endereco', 'cidade', 'estado']

class ImagemImovelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImagemImovel
        fields = '__all__' # Inclui todos os campos do modelo

class MensagemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mensagem
        fields = '__all__' # Inclui todos os campos do modelo
        read_only_fields = ['remetente', 'enviado_em']  # O remetente será preenchido automaticamente
