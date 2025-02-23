from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    telefone = models.CharField(max_length=15, blank=True, null=True)
    foto_perfil = models.ImageField(upload_to='usuarios/fotos/', blank=True, null=True)

    def __str__(self):
        return self.username


class Imovel(models.Model):
    TIPO_CHOICES = [
        ('Casa', 'Casa'),
        ('Apartamento', 'Apartamento'),
        ('Terreno', 'Terreno'),
        ('Comercial', 'Comercial'),
    ]

    titulo = models.CharField(max_length=255)
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=50)
    quartos = models.PositiveIntegerField()
    banheiros = models.PositiveIntegerField()
    area = models.PositiveIntegerField(help_text="Área em m²")
    criado_em = models.DateTimeField(auto_now_add=True)
    dono = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="imoveis")

    def __str__(self):
        return f"{self.titulo} - {self.cidade}/{self.estado}"


class ImagemImovel(models.Model):
    imovel = models.ForeignKey(Imovel, on_delete=models.CASCADE, related_name="imagens")
    imagem = models.ImageField(upload_to='imoveis/')
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Imagem de {self.imovel.titulo}"

class Mensagem(models.Model):
    remetente = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="mensagens_enviadas")
    destinatario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="mensagens_recebidas")
    imovel = models.ForeignKey(Imovel, on_delete=models.CASCADE, related_name="mensagens")
    conteudo = models.TextField()
    enviado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Mensagem de {self.remetente} para {self.destinatario} sobre {self.imovel.titulo}"

