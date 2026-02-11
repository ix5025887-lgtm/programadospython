from .base_service import BaseService
from core.models import Venda, Estoque


class VendaService(BaseService):

    def __init__(self):
        super().__init__(Venda)

    def registrar_venda(self, produto_id, quantidade):

        estoque = Estoque.objects.get(produto_id=produto_id)

        if quantidade > estoque.quantidade:
            raise ValueError("Estoque insuficiente")

        produto = estoque.produto
        valor_total = produto.preco * quantidade

        estoque.quantidade -= quantidade
        estoque.save()

        return Venda.objects.create(
            produto=produto,
            quantidade=quantidade,
            valor_total=valor_total
        )
