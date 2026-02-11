from .base_service import BaseService
from core.models import Produto


class ProdutoService(BaseService):

    def __init__(self):
        super().__init__(Produto)

    def cadastrar(self, **dados):
        return self.model.objects.create(**dados)

    def listar(self):
        return self.model.objects.all()
