from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CarroArriendoViewSet,
    CarroItemViewSet,
    CategoriaViewSet,
    ContratoViewSet,
    MaquinariaViewSet,
)

router = DefaultRouter()
router.register(r'categorias', CategoriaViewSet)
router.register(r'maquinarias', MaquinariaViewSet)
router.register(r'carro', CarroArriendoViewSet, basename='carro')
router.register(r'carro-items', CarroItemViewSet, basename='carro-items')
router.register(r'contratos', ContratoViewSet, basename='contratos')

urlpatterns = [
    path('', include(router.urls)),
]