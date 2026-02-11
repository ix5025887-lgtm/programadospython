from rest_framework.routers import DefaultRouter
from .views import ProdutoViewSet, EstoqueViewSet, VendaViewSet

router = DefaultRouter()
router.register(r'produtos', ProdutoViewSet)
router.register(r'estoques', EstoqueViewSet)
router.register(r'vendas', VendaViewSet)

urlpatterns = router.urls
