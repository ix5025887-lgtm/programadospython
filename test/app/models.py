from django.db import models
from django.utils import timezone


class Produto(models.Model):
    """Modelo de Produto com auditoria de timestamps"""
    codigo = models.IntegerField(unique=True)
    nome = models.CharField(max_length=100)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    criado_em = models.DateTimeField(default=timezone.now, editable=False)
    atualizado_em = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.codigo} - {self.nome}"
    
    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'
        ordering = ['codigo']


class Estoque(models.Model):
    """Modelo de Estoque com auditoria de timestamps"""
    produto = models.OneToOneField(Produto, on_delete=models.CASCADE)
    quantidade = models.IntegerField(default=0)
    criado_em = models.DateTimeField(default=timezone.now, editable=False)
    atualizado_em = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.produto.nome} - {self.quantidade} unidades"
    
    class Meta:
        verbose_name = 'Estoque'
        verbose_name_plural = 'Estoque'


class Venda(models.Model):
    """Modelo de Venda com auditoria de timestamps"""
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT)
    quantidade = models.IntegerField()
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)
    data = models.DateTimeField(auto_now_add=True)
    criado_em = models.DateTimeField(default=timezone.now, editable=False)
    atualizado_em = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Venda #{self.id} - {self.produto.nome}"
    
    class Meta:
        verbose_name = 'Venda'
        verbose_name_plural = 'Vendas'
        ordering = ['-data']
