from django.shortcuts import render, redirect
from .models import Produto, Estoque, Venda
from django.db.models import Sum

def dashboard(request):
    return render(request, 'cantina/dashboard.html', {
        'total_produtos': Produto.objects.count(),
        'total_estoque': Estoque.objects.aggregate(Sum('quantidade'))['quantidade__sum'] or 0,
        'total_vendas': Venda.objects.aggregate(Sum('valor_total'))['valor_total__sum'] or 0,
    })

def lista_produtos(request):
    return render(request, 'cantina/lista_produtos.html', {'produtos': Produto.objects.all()})

def novo_produto(request):
    if request.method == 'POST':
        Produto.objects.create(codigo=request.POST['codigo'], nome=request.POST['nome'], preco=request.POST['preco'])
        return redirect('lista-produtos')
    return render(request, 'cantina/novo_produto.html')

def lista_estoque(request):
    return render(request, 'cantina/lista_estoque.html', {'estoques': Estoque.objects.all()})

def entrada_estoque(request):
    if request.method == 'POST':
        produto = Produto.objects.get(id=request.POST['produto_id'])
        estoque, _ = Estoque.objects.get_or_create(produto=produto)
        estoque.quantidade += int(request.POST['quantidade'])
        estoque.save()
        return redirect('lista-estoque')
    return render(request, 'cantina/entrada_estoque.html', {'produtos': Produto.objects.all()})

def lista_vendas(request):
    return render(request, 'cantina/lista_vendas.html', {'vendas': Venda.objects.all()})

def registrar_venda(request):
    if request.method == 'POST':
        produto = Produto.objects.get(id=request.POST['produto_id'])
        quantidade = int(request.POST['quantidade'])
        try:
            estoque = Estoque.objects.get(produto=produto)
        except Estoque.DoesNotExist:
            return render(request, 'cantina/registrar_venda.html', {'produtos': Produto.objects.all(), 'erro': 'Produto sem estoque'})
        if quantidade > estoque.quantidade:
            return render(request, 'cantina/registrar_venda.html', {'produtos': Produto.objects.all(), 'erro': 'Estoque insuficiente'})
        Venda.objects.create(produto=produto, quantidade=quantidade, valor_unitario=produto.preco)
        estoque.quantidade -= quantidade
        estoque.save()
        return redirect('lista-vendas')
    return render(request, 'cantina/registrar_venda.html', {'produtos': Produto.objects.all()})
