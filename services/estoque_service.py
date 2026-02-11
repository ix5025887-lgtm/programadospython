from services.base_service import BaseService
from functionalities import log_operacao

class EstoqueService(BaseService):

    def listar(self):
        self.cursor.execute("SELECT * FROM estoque")
        return self.cursor.fetchall()

    @log_operacao
    def entrada_produto(self, codigo, quantidade):

        self.cursor.execute(
            "SELECT Produto, Preço FROM produtos WHERE Código = %s",
            (codigo,)
        )
        produto = self.cursor.fetchone()

        if not produto:
            print("❌ Produto não cadastrado. Cadastre o produto primeiro.")
            return


        self.cursor.execute(
            "SELECT Quantidade_Estoque FROM estoque WHERE Código = %s",
            (codigo,)
        )
        estoque = self.cursor.fetchone()

        if estoque:
            self.cursor.execute(
                """
                UPDATE estoque
                SET Quantidade_Estoque = Quantidade_Estoque + %s
                WHERE Código = %s
                """,
                (quantidade, codigo)
            )
        else:
            self.cursor.execute(
                """
                INSERT INTO estoque (Código, Produto, Preço, Quantidade_Estoque)
                VALUES (%s, %s, %s, %s)
                """,
                (codigo, produto[0], produto[1], quantidade)
            )

        self.con.commit()
        print("✅ Estoque atualizado com sucesso!")
