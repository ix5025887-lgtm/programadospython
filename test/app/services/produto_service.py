"""
Serviço de Produtos
Responsável por operações com produtos
"""

from typing import Optional
from decimal import Decimal
from django.db.models import QuerySet

from .base_service import BaseService
from app.decorators import log_operacao
from app.models import Produto


class ProdutoService(BaseService):
    """Serviço para gerenciar produtos"""
    
    @log_operacao
    def cadastrar(self, codigo: int, nome: str, preco: Decimal) -> Produto:
        """
        Cadastra um novo produto
        
        Args:
            codigo (int): Código único do produto
            nome (str): Nome do produto
            preco (float): Preço do produto
            
        Returns:
            Produto: Objeto criado
        """
        self._validar_dados(codigo=codigo, nome=nome, preco=preco)
        
        if Produto.objects.filter(codigo=codigo).exists():
            raise ValueError(f"Produto com código {codigo} já existe")
        
        produto = Produto.objects.create(
            codigo=codigo,
            nome=nome,
            preco=preco
        )
        return produto
    
    def listar(self) -> QuerySet[Produto]:
        """
        Lista todos os produtos
        
        Returns:
            QuerySet: Lista de produtos
        """
        return Produto.objects.all().order_by('codigo')
    
    @log_operacao
    def atualizar(self, codigo: int, nome: Optional[str] = None, preco: Optional[Decimal] = None) -> Produto:
        """
        Atualiza um produto existente
        
        Args:
            codigo (int): Código do produto
            nome (str): Novo nome (opcional)
            preco (float): Novo preço (opcional)
            
        Returns:
            Produto: Objeto atualizado
        """
        try:
            produto = Produto.objects.get(codigo=codigo)
            
            if nome:
                produto.nome = nome
            if preco:
                produto.preco = preco
                
            produto.save()
            return produto
        except Produto.DoesNotExist:
            raise ValueError(f"Produto com código {codigo} não encontrado")
    
    @log_operacao
    def deletar(self, codigo: int) -> bool:
        """
        Deleta um produto
        
        Args:
            codigo (int): Código do produto
            
        Returns:
            bool: True se deletado
        """
        try:
            Produto.objects.get(codigo=codigo).delete()
            return True
        except Produto.DoesNotExist:
            raise ValueError(f"Produto com código {codigo} não encontrado")
    
    def obter_por_codigo(self, codigo: int) -> Optional[Produto]:
        """
        Obtém um produto pelo código
        
        Args:
            codigo (int): Código do produto
            
        Returns:
            Produto: Objeto ou None
        """
        try:
            return Produto.objects.get(codigo=codigo)
        except Produto.DoesNotExist:
            return None
