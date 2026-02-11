from rest_framework import serializers
from .models import Produto, Estoque, Venda


class ProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = "__all__"


class EstoqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estoque
        fields = "__all__"


class VendaSerializer(serializers.ModelSerializer):
    valor_total = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True
    )

    class Meta:
        model = Venda
        fields = '__all__'

