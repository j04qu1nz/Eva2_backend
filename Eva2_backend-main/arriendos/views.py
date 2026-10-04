from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import Maquinaria, Categoria
from .serializers import MaquinariaSerializer

class MaquinariaViewSet(viewsets.ModelViewSet):
    queryset = Maquinaria.objects.all()
    serializer_class = MaquinariaSerializer
    permission_classes = [AllowAny]

@csrf_exempt
def catalogo_view(request):
    maquinarias = Maquinaria.objects.all()
    categorias = Categoria.objects.all()
    return render(request, 'maquinarias.html', {
        'maquinarias': maquinarias,
        'categorias': categorias
    })