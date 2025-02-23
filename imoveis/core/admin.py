from django.contrib import admin
from .models import Usuario, Imovel, ImagemImovel, Mensagem

admin.site.register(Usuario)
admin.site.register(Imovel)
admin.site.register(ImagemImovel)
admin.site.register(Mensagem)
