"""
Serviço de Vendas
Responsável por operações com vendas
"""

from typing import Optional
from decimal import Decimal
from django.db.models import QuerySet

from .base_service import BaseService
from .estoque_service import EstoqueService
from app.decorators import log_operacao
from app.models import Venda, Estoque, Produto


class VendaService(BaseService):
    """Serviço para gerenciar vendas"""
    
    def __init__(self) -> None:
        super().__init__()
        self.estoque_service = EstoqueService()
    
    @log_operacao
    def registrar_venda(self, codigo: int, quantidade: int) -> Venda:
        """
        Registra uma venda e atualiza estoque
        
        Args:
            codigo (int): Código do produto
            quantidade (int): Quantidade vendida
            
        Returns:
            Venda: Objeto venda criado
        """
        self._validar_dados(codigo=codigo, quantidade=quantidade)
        
        # Obtém o produto
        try:
            produto = Produto.objects.get(codigo=codigo)
        except Produto.DoesNotExist:
            raise ValueError(f"Produto com código {codigo} não encontrado")
        
        # Verifica estoque
        quantidade_int = int(quantidade)
        estoque = Estoque.objects.filter(produto=produto).first()
        
        if not estoque or estoque.quantidade < quantidade_int:
            disponivel = estoque.quantidade if estoque else 0
            raise ValueError(
                f"Estoque insuficiente. Solicitado: {quantidade_int}, "
                f"Disponível: {disponivel}"
            )
        
        # Calcula valor total
        valor_total = produto.preco * Decimal(str(quantidade_int))
        
        # Cria a venda
        venda = Venda.objects.create(
            produto=produto,
            quantidade=quantidade_int,
            valor_total=valor_total
        )
        
        # Atualiza estoque
        self.estoque_service.saida_produto(codigo, quantidade_int)
        
        return venda
    
    def listar(self) -> QuerySet[Venda]:
        """
        Lista todas as vendas
        
        Returns:
            QuerySet: Lista de vendas
        """
        return Venda.objects.select_related('produto').order_by('-data')
    
    def total_vendido(self) -> Decimal:
        """
        Calcula total de vendas
        
        Returns:
            Decimal: Total de todas as vendas
        """
        from django.db.models import Sum
        total = Venda.objects.aggregate(Sum('valor_total'))
        return total['valor_total__sum'] or Decimal('0.00')
    
    def vendas_por_produto(self, codigo: int) -> QuerySet[Venda]:
        """
        Lista vendas de um produto específico
        
        Args:
            codigo (int): Código do produto
            
        Returns:
            QuerySet: Vendas do produto
        """
        return Venda.objects.filter(
            produto__codigo=codigo
        ).order_by('-data')
    
    @log_operacao
    def gerar_relatorio(self) -> dict:
        """
        Gera relatório completo de vendas.
        
        Returns:
            dict: Dados do relatório incluindo total_vendido, 
                  quantidade_evento e preco_medio
        """
        from django.db.models import Sum, Count
        
        # Agrega dados de vendas do banco
        vendas = Venda.objects.aggregate(
            total_vendas=Sum('valor_total'),
            quantidade_vendas=Count('id')
        )
        
        # Calcula preço médio
        total = vendas['total_vendas'] or Decimal('0.00')
        quantidade = vendas['quantidade_vendas'] or 0
        
        preco_medio = (
            total / quantidade if quantidade > 0 else Decimal('0.00')
        )
        
        return {
            'total_vendido': total,
            'quantidade_evento': quantidade,
            'preco_medio': preco_medio
        }
