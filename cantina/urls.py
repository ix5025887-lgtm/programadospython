from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('produtos/', views.lista_produtos, name='lista-produtos'),
    path('produtos/novo/', views.novo_produto, name='novo-produto'),
    path('estoque/', views.lista_estoque, name='lista-estoque'),
    path('estoque/entrada/', views.entrada_estoque, name='entrada-estoque'),
    path('vendas/', views.lista_vendas, name='lista-vendas'),
    path('vendas/registrar/', views.registrar_venda, name='registrar-venda'),
]
