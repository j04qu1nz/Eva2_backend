from rest_framework import serializers
from .models import Categoria, Maquinaria, CarroArriendo, CarroItem, Contrato


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'


class MaquinariaSerializer(serializers.ModelSerializer):
    categoria_nombre = serializers.ReadOnlyField(source='categoria.nombre')

    class Meta:
        model = Maquinaria
        fields = '__all__'


class CarroItemSerializer(serializers.ModelSerializer):
    maquinaria_nombre = serializers.ReadOnlyField(source='maquinaria.nombre')
    precio_diario = serializers.ReadOnlyField(source='maquinaria.precio_diario')
    subtotal = serializers.ReadOnlyField()

    class Meta:
        model = CarroItem
        fields = ['id', 'maquinaria', 'maquinaria_nombre', 'precio_diario', 'dias', 'subtotal']


class CarroArriendoSerializer(serializers.ModelSerializer):
    items = CarroItemSerializer(many=True, read_only=True)
    total = serializers.SerializerMethodField()

    class Meta:
        model = CarroArriendo
        fields = ['id', 'usuario', 'creado_en', 'items', 'total']

    def get_total(self, obj):
        return sum(item.subtotal for item in obj.items.all())


class ContratoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contrato
        fields = '__all__'