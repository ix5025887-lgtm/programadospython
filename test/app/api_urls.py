"""
URLs da API REST

Registra os ViewSets na API.
Disponibiliza endpoints: /api/produtos/, /api/estoques/, /api/vendas/
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api import ProdutoViewSet, EstoqueViewSet, VendaViewSet

# Router automaticamente cria URLs para CRUD
router = DefaultRouter()
router.register(r'produtos', ProdutoViewSet, basename='produto-api')
router.register(r'estoques', EstoqueViewSet, basename='estoque-api')
router.register(r'vendas', VendaViewSet, basename='venda-api')

# URLs da API
app_name = 'api'
urlpatterns = [
    path('', include(router.urls)),
]
