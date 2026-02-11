from .produto_service import ProdutoService
from .estoque_service import EstoqueService
from .venda_service import VendaService


class ServiceFactory:

    @staticmethod
    def criar_servico(tipo):

        if tipo == "produto":
            return ProdutoService()

        elif tipo == "estoque":
            return EstoqueService()

        elif tipo == "venda":
            return VendaService()

        else:
            raise ValueError("Serviço inválido")
