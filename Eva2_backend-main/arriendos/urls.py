from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import MaquinariaViewSet, catalogo_view

router = DefaultRouter()
router.register(r'maquinarias', MaquinariaViewSet, basename='maquinaria')

urlpatterns = [
    # Rutas de la API (ej: /api/maquinarias/)
    path('api/', include(router.urls)),

    # Vista HTML del catálogo (ej: /catalogo/)
    path('catalogo/', catalogo_view, name='catalogo'),
]