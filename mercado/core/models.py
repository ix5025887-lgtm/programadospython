from django.db import models


class Produto(models.Model):
    codigo = models.IntegerField(unique=True)
    nome = models.CharField(max_length=100)
    preco = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nome


class Estoque(models.Model):
    produto = models.OneToOneField(
        Produto,
        on_delete=models.CASCADE,
        related_name="estoque"
    )
    quantidade = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.produto.nome} - {self.quantidade}"


class Venda(models.Model):
    produto = models.ForeignKey(
        Produto,
        on_delete=models.CASCADE,
        related_name="vendas"
    )
    quantidade = models.IntegerField()
    valor_total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        editable=False  
    )
    data = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        
        self.valor_total = self.produto.preco * self.quantidade
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Venda - {self.produto.nome}"
