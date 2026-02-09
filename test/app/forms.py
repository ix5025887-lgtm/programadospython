from django import forms
from .models import Produto, Estoque, Venda

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['codigo', 'nome', 'preco']
        widgets = {
            'codigo': forms.NumberInput(attrs={'class': 'form-input'}),
            'nome': forms.TextInput(attrs={'class': 'form-input'}),
            'preco': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01'}),
        }

class EstoqueForm(forms.Form):
    produto = forms.ModelChoiceField(queryset=Produto.objects.all())
    quantidade = forms.IntegerField(min_value=1)

class VendaForm(forms.Form):
    produto = forms.ModelChoiceField(queryset=Estoque.objects.filter(quantidade__gt=0))
    quantidade = forms.IntegerField(min_value=1)
