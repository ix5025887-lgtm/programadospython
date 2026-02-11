from .base_service import BaseService
from core.models import Estoque, Produto


class EstoqueService(BaseService):

    def __init__(self):
        super().__init__(Estoque)

    def entrada_produto(self, produto_id, quantidade):

        produto = Produto.objects.get(id=produto_id)

        estoque, created = Estoque.objects.get_or_create(
            produto=produto
        )

        estoque.quantidade += quantidade
        estoque.save()

        return estoque
