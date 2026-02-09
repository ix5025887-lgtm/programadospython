from django.contrib import admin
from .models import Produto, Estoque, Venda


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    """Admin para gerenciar produtos"""
    list_display = ['codigo', 'nome', 'preco', 'criado_em', 'atualizado_em']
    search_fields = ['nome', 'codigo']
    list_filter = ['codigo', 'criado_em']
    readonly_fields = ['criado_em', 'atualizado_em']


@admin.register(Estoque)
class EstoqueAdmin(admin.ModelAdmin):
    """Admin para gerenciar estoque"""
    list_display = ['produto', 'quantidade', 'criado_em', 'atualizado_em']
    search_fields = ['produto__nome']
    list_filter = ['quantidade', 'criado_em']
    readonly_fields = ['criado_em', 'atualizado_em']


@admin.register(Venda)
class VendaAdmin(admin.ModelAdmin):
    """Admin para gerenciar vendas"""
    list_display = ['id', 'produto', 'quantidade', 'valor_total', 'data', 'criado_em']
    list_filter = ['data', 'criado_em']
    search_fields = ['produto__nome']
    readonly_fields = ['criado_em', 'atualizado_em', 'data']
    readonly_fields = ['data']
