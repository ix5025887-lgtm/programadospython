"""
Factory Pattern para criação de serviços
"""

from .produto_service import ProdutoService
from .estoque_service import EstoqueService
from .venda_service import VendaService


class ServiceFactory:
    """Fábrica para criar instâncias de serviços"""
    
    @staticmethod
    def criar_servico(tipo):
        """
        Cria uma instância de serviço conforme o tipo
        
        Args:
            tipo (str): Tipo do serviço
                - 'produto': ProdutoService
                - 'estoque': EstoqueService
                - 'venda': VendaService
        
        Returns:
            BaseService: Instância do serviço
            
        Raises:
            ValueError: Se tipo de serviço inválido
        """
        servicios = {
            'produto': ProdutoService,
            'estoque': EstoqueService,
            'venda': VendaService,
        }
        
        if tipo not in servicios:
            raise ValueError(
                f"Serviço inválido: {tipo}. "
                f"Opções: {', '.join(servicios.keys())}"
            )
        
        return servicios[tipo]()


__all__ = [
    'ServiceFactory',
    'ProdutoService',
    'EstoqueService',
    'VendaService',
]
