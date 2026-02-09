from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('produtos/', views.produtos, name='produtos'),
    path('estoque/', views.estoque, name='estoque'),
    path('vendas/', views.vendas, name='vendas'),
]
