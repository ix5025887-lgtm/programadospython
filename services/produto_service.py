from services.base_service import BaseService
from functionalities import log_operacao

class ProdutoService(BaseService):

    @log_operacao
    def cadastrar(self, codigo, produto, preco):
        sql = """
        INSERT INTO produtos (Código, Produto, Preço)
        VALUES (%s, %s, %s)
        """
        self.cursor.execute(sql, (codigo, produto, preco))
        self.con.commit()

    def listar(self):
        self.cursor.execute("SELECT * FROM produtos")
        return self.cursor.fetchall()
