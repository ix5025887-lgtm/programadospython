from django.contrib import admin
from .models import Produto, Estoque, Venda

admin.site.register(Produto)
admin.site.register(Estoque)
admin.site.register(Venda)
