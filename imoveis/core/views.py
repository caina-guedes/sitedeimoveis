# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.parsers import MultiPartParser, FormParser
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from core.models import Imovel, ImagemImovel, Mensagem
from .serializers import ImovelSerializer, ImagemImovelSerializer, MensagemSerializer



from .serializers import UsuarioSerializer

Usuario = get_user_model()  # Obtém o modelo de usuário personalizado


class ImovelListCreateAPIView(APIView):
    def get(self, request):  
        filtros = Q()  # Criamos um objeto Q vazio para armazenar os filtros

        # 🏠 Filtros opcionais (pegamos os valores da URL)
        titulo = request.GET.get('titulo')
        tipo = request.GET.get('tipo')
        min_preco = request.GET.get('min_preco')
        max_preco = request.GET.get('max_preco')
        quartos = request.GET.get('quartos')

        # Aplicamos os filtros apenas se forem informados
        if titulo:
            filtros &= Q(titulo__icontains=titulo) | Q(descricao__icontains=titulo)
        if tipo:
            filtros &= Q(tipo=tipo)
        if min_preco:
            filtros &= Q(preco__gte=min_preco)
        if max_preco:
            filtros &= Q(preco__lte=max_preco)
        if quartos:
            filtros &= Q(quartos=quartos)

        # Aplicamos os filtros diretamente no banco de dados
        imoveis = Imovel.objects.filter(filtros)

        serializer = ImovelSerializer(imoveis, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request): # Cria um novo imóvel
        serializer = ImovelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ImagemImovelListCreateAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)  # Para suportar upload de arquivos

    def get(self, request):
        imagens = ImagemImovel.objects.all()
        serializer = ImagemImovelSerializer(imagens, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ImagemImovelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class MensagemAPIView(APIView):
    permission_classes = [IsAuthenticated]  # Apenas usuários autenticados podem acessar

    def get(self, request):
        """
        Retorna todas as mensagens recebidas pelo usuário autenticado.
        """
        mensagens = Mensagem.objects.filter(destinatario=request.user).order_by('-enviado_em')
        serializer = MensagemSerializer(mensagens, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Envia uma nova mensagem para outro usuário.
        O remetente será automaticamente o usuário autenticado.
        """
        data = request.data.copy()  # Faz uma cópia dos dados da requisição
        data['remetente'] = request.user.id  # Define o remetente como o usuário autenticado

        serializer = MensagemSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ImovelDetailAPIView(APIView):
    def get(self, request, pk): # Retorna um imóvel específico
        imovel = get_object_or_404(Imovel, pk=pk)
        serializer = ImovelSerializer(imovel)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk): # Atualiza um Imóvel Específico inteiro
        imovel = get_object_or_404(Imovel, pk=pk)
        serializer = ImovelSerializer(imovel, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
  
    def patch(self, request, pk, format=None): # Atualiza os Campos Fornecidos do Imovel
        imovel = get_object_or_404(Imovel , pk = pk)
        serializer = ImovelSerializer(imovel, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
    def delete(self, request, pk): # Deleta um imóvel
        imovel = get_object_or_404(Imovel, pk=pk)
        imovel.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UsuarioAPIView(APIView):
    def get(self, request):
        """
        Retorna a lista de todos os usuários cadastrados.
        """
        usuarios = Usuario.objects.all()
        serializer = UsuarioSerializer(usuarios, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        Cria um novo usuário com os dados fornecidos.
        """
        serializer = UsuarioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
