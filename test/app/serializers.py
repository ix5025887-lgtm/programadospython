"""
Serializers para REST API

Responsável por converter modelos Django em JSON e vice-versa.
Valida dados automaticamente conforme definição dos campos.
"""

from rest_framework import serializers
from typing import Dict, Any
from .models import Produto, Estoque, Venda


class ProdutoSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo Produto.
    
    Converte objetos Produto para JSON e valida dados de entrada.
    Inclui timestamps de auditoria (criado_em, atualizado_em).
    """
    
    class Meta:
        model = Produto
        fields = ['id', 'codigo', 'nome', 'preco', 'criado_em', 'atualizado_em']
        read_only_fields = ['id', 'criado_em', 'atualizado_em']
    
    def validate_codigo(self, valor: int) -> int:
        """
        Valida se código é único (exceto na atualização).
        
        Args:
            valor (int): Código do produto
            
        Returns:
            int: Código validado
            
        Raises:
            serializers.ValidationError: Se código já existe
        """
        # Permite edição do mesmo código durante update
        if self.instance:
            if Produto.objects.filter(codigo=valor).exclude(id=self.instance.id).exists():
                raise serializers.ValidationError("Produto com este código já existe.")
        else:
            if Produto.objects.filter(codigo=valor).exists():
                raise serializers.ValidationError("Produto com este código já existe.")
        return valor
    
    def validate_preco(self, valor: float) -> float:
        """
        Valida se preço é positivo.
        
        Args:
            valor (float): Preço do produto
            
        Returns:
            float: Preço validado
            
        Raises:
            serializers.ValidationError: Se preço <= 0
        """
        if valor <= 0:
            raise serializers.ValidationError("Preço deve ser maior que zero.")
        return valor


class EstoqueSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo Estoque.
    
    Mostra também dados do produto relacionado.
    Inclui timestamps de auditoria.
    """
    
    # Aninha dados do produto na resposta
    produto = ProdutoSerializer(read_only=True)
    produto_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Estoque
        fields = ['id', 'produto', 'produto_id', 'quantidade', 'criado_em', 'atualizado_em']
        read_only_fields = ['id', 'criado_em', 'atualizado_em']
    
    def validate_quantidade(self, valor: int) -> int:
        """
        Valida se quantidade é não-negativa.
        
        Args:
            valor (int): Quantidade
            
        Returns:
            int: Quantidade validada
            
        Raises:
            serializers.ValidationError: Se quantidade < 0
        """
        if valor < 0:
            raise serializers.ValidationError("Quantidade não pode ser negativa.")
        return valor
    
    def create(self, validated_data: Dict[str, Any]) -> Estoque:
        """Cria ou obtém estoque existente (get_or_create)."""
        produto_id = validated_data.pop('produto_id')
        estoque, _ = Estoque.objects.get_or_create(
            produto_id=produto_id,
            defaults=validated_data
        )
        return estoque


class VendaSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo Venda.
    
    Mostra também dados do produto relacionado.
    Inclui timestamps de auditoria.
    """
    
    # Aninha dados do produto na resposta
    produto = ProdutoSerializer(read_only=True)
    produto_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Venda
        fields = ['id', 'produto', 'produto_id', 'quantidade', 'valor_total', 'data', 'criado_em', 'atualizado_em']
        read_only_fields = ['id', 'valor_total', 'data', 'criado_em', 'atualizado_em']
    
    def validate_quantidade(self, valor: int) -> int:
        """
        Valida se quantidade é positiva.
        
        Args:
            valor (int): Quantidade vendida
            
        Returns:
            int: Quantidade validada
            
        Raises:
            serializers.ValidationError: Se quantidade <= 0
        """
        if valor <= 0:
            raise serializers.ValidationError("Quantidade deve ser maior que zero.")
        return valor
