"""
Testes Unitários do Sistema de Cantina

Testa models, services, serializers e API endpoints.
Rode com: python manage.py test
"""

from decimal import Decimal
from django.test import TestCase, Client
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

from .models import Produto, Estoque, Venda
from .services import ServiceFactory


# ===== TESTES DE MODELS =====

class ProdutoModelTest(TestCase):
    """Testy para o model Produto"""
    
    def setUp(self) -> None:
        """Cria dados de teste antes de cada teste"""
        self.produto = Produto.objects.create(
            codigo=1,
            nome='Hamburguer',
            preco=15.50
        )
    
    def test_criacao_produto(self) -> None:
        """Testa se produto é criado corretamente"""
        self.assertEqual(self.produto.codigo, 1)
        self.assertEqual(self.produto.nome, 'Hamburguer')
        self.assertEqual(self.produto.preco, Decimal('15.50'))
    
    def test_str_produto(self) -> None:
        """Testa representação em string do produto"""
        self.assertEqual(str(self.produto), '1 - Hamburguer')
    
    def test_codigo_unico(self) -> None:
        """Testa se código deve ser único"""
        with self.assertRaises(Exception):  # IntegrityError
            Produto.objects.create(codigo=1, nome='Outro', preco=10)


class EstoqueModelTest(TestCase):
    """Testes para o model Estoque"""
    
    def setUp(self) -> None:
        """Cria dados de teste"""
        self.produto = Produto.objects.create(codigo=1, nome='Pizza', preco=25.00)
        self.estoque = Estoque.objects.create(produto=self.produto, quantidade=10)
    
    def test_criacao_estoque(self) -> None:
        """Testa se estoque é criado"""
        self.assertEqual(self.estoque.quantidade, 10)
        self.assertEqual(self.estoque.produto, self.produto)
    
    def test_str_estoque(self) -> None:
        """Testa representação em string"""
        self.assertEqual(str(self.estoque), 'Pizza - 10 unidades')


class VendaModelTest(TestCase):
    """Testes para o model Venda"""
    
    def setUp(self) -> None:
        """Cria dados de teste"""
        self.produto = Produto.objects.create(codigo=1, nome='Suco', preco=5.00)
        self.estoque = Estoque.objects.create(produto=self.produto, quantidade=100)
        self.venda = Venda.objects.create(
            produto=self.produto,
            quantidade=5,
            valor_total=Decimal('25.00')
        )
    
    def test_criacao_venda(self) -> None:
        """Testa se venda é criada"""
        self.assertEqual(self.venda.quantidade, 5)
        self.assertEqual(self.venda.valor_total, Decimal('25.00'))
    
    def test_str_venda(self) -> None:
        """Testa representação em string"""
        self.assertIn('Suco', str(self.venda))


# ===== TESTES DE SERVICES =====

class ProdutoServiceTest(TestCase):
    """Testes para ProdutoService"""
    
    def setUp(self) -> None:
        """Cria service e dados de teste"""
        self.service = ServiceFactory.criar_servico('produto')
    
    def test_cadastrar_produto(self) -> None:
        """Testa cadastro de produto"""
        produto = self.service.cadastrar(
            codigo=10,
            nome='Batata Frita',
            preco=Decimal('8.50')
        )
        self.assertEqual(produto.codigo, 10)
        self.assertEqual(produto.nome, 'Batata Frita')
    
    def test_cadastrar_codigo_duplicado(self) -> None:
        """Testa se código duplicado gera erro"""
        self.service.cadastrar(1, 'Produto 1', Decimal('10.00'))
        
        with self.assertRaises(ValueError):
            self.service.cadastrar(1, 'Produto 2', Decimal('20.00'))
    
    def test_listar_produtos(self) -> None:
        """Testa listagem de produtos"""
        self.service.cadastrar(1, 'P1', Decimal('10.00'))
        self.service.cadastrar(2, 'P2', Decimal('20.00'))
        
        produtos = self.service.listar()
        self.assertEqual(produtos.count(), 2)
    
    def test_obter_por_codigo(self) -> None:
        """Testa busca por código"""
        self.service.cadastrar(5, 'Produto 5', Decimal('15.00'))
        
        produto = self.service.obter_por_codigo(5)
        self.assertIsNotNone(produto)
        self.assertEqual(produto.nome, 'Produto 5')


class EstoqueServiceTest(TestCase):
    """Testes para EstoqueService"""
    
    def setUp(self) -> None:
        """Cria service e dados de teste"""
        self.service = ServiceFactory.criar_servico('estoque')
        self.produto_service = ServiceFactory.criar_servico('produto')
        
        # Cria um produto
        self.produto = self.produto_service.cadastrar(1, 'Item', Decimal('10.00'))
    
    def test_entrada_produto(self) -> None:
        """Testa adição ao estoque"""
        estoque = self.service.entrada_produto(1, 50)
        self.assertEqual(estoque.quantidade, 50)
    
    def test_saida_produto(self) -> None:
        """Testa remoção do estoque"""
        self.service.entrada_produto(1, 100)
        estoque = self.service.saida_produto(1, 30)
        self.assertEqual(estoque.quantidade, 70)
    
    def test_saida_insuficiente(self) -> None:
        """Testa se saída maior que estoque gera erro"""
        self.service.entrada_produto(1, 10)
        
        with self.assertRaises(ValueError):
            self.service.saida_produto(1, 20)
    
    def test_obter_quantidade(self) -> None:
        """Testa busca de quantidade"""
        self.service.entrada_produto(1, 25)
        
        quantidade = self.service.obter_quantidade(1)
        self.assertEqual(quantidade, 25)


class VendaServiceTest(TestCase):
    """Testes para VendaService"""
    
    def setUp(self) -> None:
        """Cria service e dados de teste"""
        self.venda_service = ServiceFactory.criar_servico('venda')
        self.estoque_service = ServiceFactory.criar_servico('estoque')
        self.produto_service = ServiceFactory.criar_servico('produto')
        
        # Cria produto e estoque
        self.produto = self.produto_service.cadastrar(1, 'Lanche', Decimal('12.00'))
        self.estoque_service.entrada_produto(1, 100)
    
    def test_registrar_venda(self) -> None:
        """Testa registro de venda"""
        venda = self.venda_service.registrar_venda(1, 5)
        
        self.assertEqual(venda.quantidade, 5)
        self.assertEqual(venda.valor_total, Decimal('60.00'))
    
    def test_venda_atualiza_estoque(self) -> None:
        """Testa se venda atualiza estoque"""
        self.venda_service.registrar_venda(1, 20)
        
        quantidade = self.estoque_service.obter_quantidade(1)
        self.assertEqual(quantidade, 80)
    
    def test_total_vendido(self) -> None:
        """Testa cálculo de total"""
        self.venda_service.registrar_venda(1, 5)  # 60.00
        self.venda_service.registrar_venda(1, 3)  # 36.00
        
        total = self.venda_service.total_vendido()
        self.assertEqual(total, Decimal('96.00'))


# ===== TESTES DE API REST =====

class ProdutoAPITest(TestCase):
    """Testes para API de Produtos"""
    
    def setUp(self) -> None:
        """Cria cliente API e dados"""
        self.client = APIClient()
        self.url = reverse('api:produto-api-list')
        
        Produto.objects.create(codigo=1, nome='P1', preco=10.00)
    
    def test_listar_produtos(self) -> None:
        """Testa GET /api/produtos/"""
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_criar_produto(self) -> None:
        """Testa POST /api/produtos/"""
        dados = {'codigo': 2, 'nome': 'P2', 'preco': 20.00}
        response = self.client.post(self.url, dados)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Produto.objects.count(), 2)
    
    def test_criar_codigo_duplicado(self) -> None:
        """Testa erro ao criar com código duplicado"""
        dados = {'codigo': 1, 'nome': 'Duplicado', 'preco': 15.00}
        response = self.client.post(self.url, dados)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class EstoqueAPITest(TestCase):
    """Testes para API de Estoque"""
    
    def setUp(self) -> None:
        """Cria cliente API e dados"""
        self.client = APIClient()
        self.url = reverse('api:estoque-api-list')
        
        self.produto = Produto.objects.create(codigo=1, nome='P1', preco=10.00)
        self.estoque = Estoque.objects.create(produto=self.produto, quantidade=50)
    
    def test_listar_estoque(self) -> None:
        """Testa GET /api/estoques/"""
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_entrada_estoque(self) -> None:
        """Testa POST /api/estoques/entrada/"""
        url = reverse('api:estoque-api-entrada')
        dados = {'produto_id': self.produto.id, 'quantidade': 30}
        
        response = self.client.post(url, dados)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.estoque.refresh_from_db()
        self.assertEqual(self.estoque.quantidade, 80)


class VendaAPITest(TestCase):
    """Testes para API de Vendas"""
    
    def setUp(self) -> None:
        """Cria cliente API e dados"""
        self.client = APIClient()
        self.url = reverse('api:venda-api-list')
        
        self.produto = Produto.objects.create(codigo=1, nome='P1', preco=10.00)
        self.estoque = Estoque.objects.create(produto=self.produto, quantidade=100)
    
    def test_registrar_venda(self) -> None:
        """Testa POST /api/vendas/"""
        dados = {'produto_id': self.produto.id, 'quantidade': 5}
        response = self.client.post(self.url, dados)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Venda.objects.count(), 1)
    
    def test_listar_vendas(self) -> None:
        """Testa GET /api/vendas/"""
        # Cria uma venda
        Venda.objects.create(
            produto=self.produto,
            quantidade=5,
            valor_total=Decimal('50.00')
        )
        
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
