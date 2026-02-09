from services.estoque_service import EstoqueService
from services.venda_service import VendaService
from services.produto_service import ProdutoService

class ServiceFactory:

    @staticmethod
    def criar_servico(tipo, conexao):
        if tipo == "estoque":
            return EstoqueService(conexao)
        elif tipo == "venda":
            return VendaService(conexao)
        elif tipo == "produto":
            return ProdutoService(conexao)
        else:
            raise ValueError("Serviço inválido")
