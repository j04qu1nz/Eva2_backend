from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import CarroArriendo, CarroItem, Categoria, Contrato, Maquinaria
from .permissions import IsAdminOrReadOnly
from .serializers import (
    CarroArriendoSerializer,
    CarroItemSerializer,
    CategoriaSerializer,
    ContratoSerializer,
    MaquinariaSerializer,
)


class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [IsAdminOrReadOnly]


class MaquinariaViewSet(viewsets.ModelViewSet):
    queryset = Maquinaria.objects.all()
    serializer_class = MaquinariaSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['categoria', 'disponible']
    search_fields = ['nombre', 'descripcion']


class CarroArriendoViewSet(viewsets.ModelViewSet):
    serializer_class = CarroArriendoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CarroArriendo.objects.filter(usuario=self.request.user)

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)

    @action(detail=False, methods=['post'], url_path='checkout')
    def checkout(self, request):
        carro, _ = CarroArriendo.objects.get_or_create(usuario=request.user)
        items = carro.items.select_related('maquinaria').all()

        if not items.exists():
            return Response(
                {'detail': 'El carro está vacío.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Transacción Atómica para control estricto de Inventario/Stock
        with transaction.atomic():
            for item in items:
                maquinaria = item.maquinaria
                if not maquinaria.disponible or maquinaria.stock < 1:
                    return Response(
                        {
                            'detail': f'La maquinaria "{maquinaria.nombre}" no tiene stock disponible.'
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                # Descuento de stock
                maquinaria.stock -= 1
                if maquinaria.stock == 0:
                    maquinaria.disponible = False
                maquinaria.save()

            total = sum(item.subtotal for item in items)
            contrato = Contrato.objects.create(
                usuario=request.user, total=total, estado='PENDIENTE'
            )

            items.delete()

        serializer = ContratoSerializer(contrato)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CarroItemViewSet(viewsets.ModelViewSet):
    serializer_class = CarroItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CarroItem.objects.filter(carro__usuario=self.request.user)


class ContratoViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ContratoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Contrato.objects.all()
        return Contrato.objects.filter(usuario=self.request.user)