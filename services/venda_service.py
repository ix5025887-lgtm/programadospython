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
        
        # ===== CONFIRMAÇÃO DA VENDA =====

        print("\nResumo da venda:")
        print(f"Produto: {nome}")
        print(f"Quantidade: {quantidade}")
        print(f"Preço unitário: {preco:.2f}")
        print(f"Valor total: {total:.2f}")

        confirmar = input("Confirmar venda? (s/n): ").lower()

        if confirmar != 's':
            print("Venda cancelada.")
            return False

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
