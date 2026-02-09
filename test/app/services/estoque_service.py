"""
Serviço de Estoque
Responsável por operações com estoque
"""

from typing import Optional
from django.db.models import QuerySet

from .base_service import BaseService
from app.decorators import log_operacao
from app.models import Estoque, Produto


class EstoqueService(BaseService):
    """Serviço para gerenciar estoque"""
    
    @log_operacao
    def entrada_produto(self, codigo: int, quantidade: int) -> Estoque:
        """
        Adiciona quantidade ao estoque (entrada)
        
        Args:
            codigo (int): Código do produto
            quantidade (int): Quantidade a adicionar
            
        Returns:
            Estoque: Objeto atualizado
        """
        self._validar_dados(codigo=codigo, quantidade=quantidade)
        
        try:
            produto = Produto.objects.get(codigo=codigo)
        except Produto.DoesNotExist:
            raise ValueError(f"Produto com código {codigo} não encontrado")
        
        estoque, _ = Estoque.objects.get_or_create(produto=produto)
        estoque.quantidade += int(quantidade)
        estoque.save()
        
        return estoque
    
    @log_operacao
    def saida_produto(self, codigo: int, quantidade: int) -> Estoque:
        """
        Remove quantidade do estoque (saída)
        
        Args:
            codigo (int): Código do produto
            quantidade (int): Quantidade a remover
            
        Returns:
            Estoque: Objeto atualizado
        """
        self._validar_dados(codigo=codigo, quantidade=quantidade)
        
        try:
            estoque = Estoque.objects.get(produto__codigo=codigo)
        except Estoque.DoesNotExist:
            raise ValueError(f"Estoque do produto {codigo} não encontrado")
        
        if estoque.quantidade < int(quantidade):
            raise ValueError(f"Estoque insuficiente. Disponível: {estoque.quantidade}")
        
        estoque.quantidade -= int(quantidade)
        estoque.save()
        
        return estoque
    
    def listar(self) -> QuerySet[Estoque]:
        """
        Lista todo o estoque
        
        Returns:
            QuerySet: Lista de estoques
        """
        return Estoque.objects.select_related('produto').order_by('produto__codigo')
    
    def obter_quantidade(self, codigo: int) -> int:
        """
        Obtém quantidade em estoque de um produto
        
        Args:
            codigo (int): Código do produto
            
        Returns:
            int: Quantidade disponível
        """
        try:
            estoque = Estoque.objects.get(produto__codigo=codigo)
            return estoque.quantidade
        except Estoque.DoesNotExist:
            return 0
    
    def listar_baixo_estoque(self, limite: int = 5) -> QuerySet[Estoque]:
        """
        Lista produtos com estoque baixo
        
        Args:
            limite (int): Limite mínimo de estoque
            
        Returns:
            QuerySet: Produtos com estoque baixo
        """
        return Estoque.objects.filter(
            quantidade__lt=limite
        ).select_related('produto')
