"""
API REST - ViewSets e Endpoints

Fornece GET, POST, PUT, PATCH, DELETE para os modelos.
Usa DRF (Django REST Framework) para facilitar.
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.request import Request
from typing import Any

from .models import Produto, Estoque, Venda
from .serializers import ProdutoSerializer, EstoqueSerializer, VendaSerializer
from .services import ServiceFactory


class ProdutoViewSet(viewsets.ModelViewSet):
    """
    API para gerenciar produtos.
    
    GET /api/produtos/            - Lista todos
    POST /api/produtos/           - Cria novo
    GET /api/produtos/{id}/       - Detalha um
    PUT /api/produtos/{id}/       - Atualiza completo
    PATCH /api/produtos/{id}/     - Atualiza parcial
    DELETE /api/produtos/{id}/    - Deleta
    """
    
    queryset = Produto.objects.all().order_by('codigo')
    serializer_class = ProdutoSerializer
    
    def perform_create(self, serializer: ProdutoSerializer) -> None:
        """Hook para executar lógica customizada ao criar."""
        # Valida e cria via serializer (já validou tudo)
        serializer.save()
    
    @action(detail=False, methods=['get'])
    def por_codigo(self, request: Request) -> Response:
        """
        Busca produto por código.
        
        GET /api/produtos/por_codigo/?codigo=123
        """
        codigo = request.query_params.get('codigo')
        if not codigo:
            return Response(
                {'erro': 'Parâmetro código é obrigatório'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            produto = Produto.objects.get(codigo=codigo)
            serializer = self.get_serializer(produto)
            return Response(serializer.data)
        except Produto.DoesNotExist:
            return Response(
                {'erro': f'Produto com código {codigo} não encontrado'},
                status=status.HTTP_404_NOT_FOUND
            )


class EstoqueViewSet(viewsets.ModelViewSet):
    """
    API para gerenciar estoque.
    
    GET /api/estoques/       - Lista todos
    POST /api/estoques/      - Adiciona ao estoque
    GET /api/estoques/{id}/  - Detalha um
    PATCH /api/estoques/{id}/ - Atualiza quantidade
    """
    
    queryset = Estoque.objects.all().select_related('produto').order_by('produto__codigo')
    serializer_class = EstoqueSerializer
    
    @action(detail=False, methods=['post'])
    def entrada(self, request: Request) -> Response:
        """
        Adiciona quantidade ao estoque (entrada).
        
        POST /api/estoques/entrada/
        Body: {"produto_id": 1, "quantidade": 10}
        """
        estoque_service = ServiceFactory.criar_servico('estoque')
        
        produto_id = request.data.get('produto_id')
        quantidade = request.data.get('quantidade')
        
        if not produto_id or not quantidade:
            return Response(
                {'erro': 'Campos produto_id e quantidade são obrigatórios'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            produto = Produto.objects.get(id=produto_id)
            estoque = estoque_service.entrada_produto(produto.codigo, quantidade)
            serializer = self.get_serializer(estoque)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response(
                {'erro': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=False, methods=['post'])
    def saida(self, request: Request) -> Response:
        """
        Remove quantidade do estoque (saída).
        
        POST /api/estoques/saida/
        Body: {"produto_id": 1, "quantidade": 5}
        """
        estoque_service = ServiceFactory.criar_servico('estoque')
        
        produto_id = request.data.get('produto_id')
        quantidade = request.data.get('quantidade')
        
        if not produto_id or not quantidade:
            return Response(
                {'erro': 'Campos produto_id e quantidade são obrigatórios'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            produto = Produto.objects.get(id=produto_id)
            estoque = estoque_service.saida_produto(produto.codigo, quantidade)
            serializer = self.get_serializer(estoque)
            return Response(serializer.data)
        except ValueError as e:
            return Response(
                {'erro': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=False, methods=['get'])
    def baixo_estoque(self, request: Request) -> Response:
        """
        Lista produtos com estoque baixo.
        
        GET /api/estoques/baixo_estoque/?limite=5
        """
        estoque_service = ServiceFactory.criar_servico('estoque')
        limite = int(request.query_params.get('limite', 5))
        
        estoques = estoque_service.listar_baixo_estoque(limite)
        serializer = self.get_serializer(estoques, many=True)
        return Response(serializer.data)


class VendaViewSet(viewsets.ModelViewSet):
    """
    API para gerenciar vendas.
    
    GET /api/vendas/         - Lista todas
    POST /api/vendas/        - Cria nova venda
    GET /api/vendas/{id}/    - Detalha uma
    """
    
    queryset = Venda.objects.all().select_related('produto').order_by('-data')
    serializer_class = VendaSerializer
    
    def perform_create(self, serializer: VendaSerializer) -> None:
        """Hook que cria venda e atualiza estoque automaticamente."""
        venda_service = ServiceFactory.criar_servico('venda')
        
        produto_id = serializer.validated_data['produto_id']
        quantidade = serializer.validated_data['quantidade']
        
        try:
            produto = Produto.objects.get(id=produto_id)
            # Service cria a venda e atualiza estoque
            venda_service.registrar_venda(produto.codigo, quantidade)
        except ValueError as e:
            from rest_framework.exceptions import ValidationError
            raise ValidationError({'erro': str(e)})
    
    @action(detail=False, methods=['get'])
    def total_vendido(self, request: Request) -> Response:
        """
        Retorna total de vendas.
        
        GET /api/vendas/total_vendido/
        """
        venda_service = ServiceFactory.criar_servico('venda')
        relatorio = venda_service.gerar_relatorio()
        
        return Response({
            'total_vendido': relatorio['total_vendido'],
            'quantidade_vendas': relatorio['quantidade_evento'],
            'preco_medio': relatorio['preco_medio']
        })
    
    @action(detail=False, methods=['get'])
    def por_produto(self, request: Request) -> Response:
        """
        Lista vendas de um produto específico.
        
        GET /api/vendas/por_produto/?codigo=123
        """
        venda_service = ServiceFactory.criar_servico('venda')
        codigo = request.query_params.get('codigo')
        
        if not codigo:
            return Response(
                {'erro': 'Parâmetro código é obrigatório'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        vendas = venda_service.vendas_por_produto(int(codigo))
        serializer = self.get_serializer(vendas, many=True)
        return Response(serializer.data)
