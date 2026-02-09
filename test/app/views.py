"""
Views do Sistema de Cantina Escolar

Responsável pelas requisições HTTP e renderização dos templates.
Usa ServiceFactory para acessar a lógica de negócio.
"""

from typing import Dict, Any
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib import messages
from .models import Produto, Estoque, Venda
from .forms import ProdutoForm, EstoqueForm, VendaForm
from .services import ServiceFactory


def home(request: HttpRequest) -> HttpResponse:
    """
    Página inicial do sistema.
    
    Args:
        request (HttpRequest): Requisição HTTP
        
    Returns:
        HttpResponse: Template home.html renderizado
    """
    return render(request, 'home.html')


def produtos(request: HttpRequest) -> HttpResponse:
    """
    Gestão de produtos - listar e cadastrar.
    
    Args:
        request (HttpRequest): Requisição HTTP
        
    Returns:
        HttpResponse: Template produtos.html com lista e formulário
    """
    # Factory cria instância do serviço de produtos
    produto_service = ServiceFactory.criar_servico('produto')
    
    if request.method == 'POST':
        form = ProdutoForm(request.POST)
        if form.is_valid():
            try:
                # Extrai dados validados do formulário
                codigo = form.cleaned_data['codigo']
                nome = form.cleaned_data['nome']
                preco = form.cleaned_data['preco']
                
                # Delega lógica de cadastro para o serviço
                # (validação de código único, etc)
                produto_service.cadastrar(codigo, nome, preco)
                messages.success(request, 'Produto cadastrado com sucesso!')
                return redirect('produtos')
            except ValueError as e:
                # Captura erros de negócio (código duplicado, etc)
                messages.error(request, str(e))
        else:
            # Formulário com erros de validação (campos obrigatórios, tipos, etc)
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = ProdutoForm()
    
    # Obtém lista de produtos do serviço
    produtos = produto_service.listar()
    return render(request, 'produtos.html', {'form': form, 'produtos': produtos})



def estoque(request: HttpRequest) -> HttpResponse:
    """
    Gestão de estoque - adicionar produtos.
    
    Args:
        request (HttpRequest): Requisição HTTP
        
    Returns:
        HttpResponse: Template estoque.html com formulário e lista
    """
    # Factory cria instância do serviço de estoque
    estoque_service = ServiceFactory.criar_servico('estoque')
    
    if request.method == 'POST':
        form = EstoqueForm(request.POST)
        if form.is_valid():
            try:
                # Extrai dados validados
                produto = form.cleaned_data['produto']
                quantidade = form.cleaned_data['quantidade']
                
                # Chama serviço para adicionar ao estoque
                # (verifica se produto existe, etc)
                estoque_service.entrada_produto(produto.codigo, quantidade)
                messages.success(request, 'Estoque atualizado!')
                return redirect('estoque')
            except ValueError as e:
                messages.error(request, str(e))
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = EstoqueForm()
    
    # Obtém lista completa de estoque
    estoque = estoque_service.listar()
    return render(request, 'estoque.html', {'form': form, 'estoque': estoque})



def vendas(request: HttpRequest) -> HttpResponse:
    """
    Gestão de vendas - registrar vendas e visualizar relatórios.
    
    Args:
        request (HttpRequest): Requisição HTTP
        
    Returns:
        HttpResponse: Template vendas.html com formulário, lista e relatórios
    """
    # Factory cria instância do serviço de vendas
    venda_service = ServiceFactory.criar_servico('venda')
    
    if request.method == 'POST':
        form = VendaForm(request.POST)
        if form.is_valid():
            try:
                # Extrai dados validados
                estoque_obj = form.cleaned_data['produto']
                quantidade = form.cleaned_data['quantidade']
                
                # Chama serviço para registrar venda
                # (verifica estoque suficiente, atualiza automaticamente)
                venda_service.registrar_venda(estoque_obj.produto.codigo, quantidade)
                messages.success(request, 'Venda registrada!')
                return redirect('vendas')
            except ValueError as e:
                messages.error(request, str(e))
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = VendaForm()
    
    # Obtém lista de vendas e gera relatório
    vendas = venda_service.listar()
    relatorio = venda_service.gerar_relatorio()
    
    return render(request, 'vendas.html', {
        'form': form,
        'vendas': vendas,
        'total': relatorio['total_vendido'],
        'quantidade': relatorio['quantidade_evento']
    })
