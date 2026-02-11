from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Produto, Estoque, Venda
from .serializers import ProdutoSerializer, EstoqueSerializer, VendaSerializer
from .services.factory import ServiceFactory
from django.http import HttpResponse
from rest_framework.exceptions import ValidationError
from core.models import Estoque

def home(request):
    return HttpResponse("Sistema de Mercado API rodando 🚀")


class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer


class EstoqueViewSet(viewsets.ModelViewSet):
    queryset = Estoque.objects.all()
    serializer_class = EstoqueSerializer


class VendaViewSet(viewsets.ModelViewSet):
    queryset = Venda.objects.all()
    serializer_class = VendaSerializer

    def perform_create(self, serializer):
        produto = serializer.validated_data['produto']
        quantidade = serializer.validated_data['quantidade']

        try:
            estoque = Estoque.objects.get(produto=produto)
        except Estoque.DoesNotExist:
            raise ValidationError("Este produto não possui estoque cadastrado.")

        if quantidade > estoque.quantidade:
            raise ValidationError("Estoque insuficiente.")

        estoque.quantidade -= quantidade
        estoque.save()

        serializer.save()
