from services.base_service import BaseService
from functionalities import log_operacao

class VendaService(BaseService):

    @log_operacao
    def registrar_venda(self, codigo, quantidade):
        self.cursor.execute(
            """
            SELECT Produto, Preço, Quantidade_Estoque
            FROM estoque
            WHERE Código = %s
            """,
            (codigo,)
        )
        produto = self.cursor.fetchone()

        if not produto:
            print("❌ Produto não encontrado no estoque.")
            return False

        nome, preco, estoque_atual = produto

        if quantidade > estoque_atual:
            print("❌ Estoque insuficiente.")
            return False

        total = preco * quantidade

        self.cursor.execute(
            """
            INSERT INTO vendas
            (Código, Produto, Preço, Quantidade_Vendas, Valor_Total_Vendido)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (codigo, nome, preco, quantidade, total)
        )

        self.cursor.execute(
            """
            UPDATE estoque
            SET Quantidade_Estoque = Quantidade_Estoque - %s
            WHERE Código = %s
            """,
            (quantidade, codigo)
        )

        self.con.commit()
        print("✅ Venda realizada com sucesso!")
        return True
