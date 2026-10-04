from django.contrib.auth.models import User
from django.db import models


class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre


class Maquinaria(models.Model):
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True, null=True)
    precio_diario = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=1)
    disponible = models.BooleanField(default=True)
    categoria = models.ForeignKey(
        Categoria, on_delete=models.CASCADE, related_name='maquinarias'
    )

    def __str__(self):
        return self.nombre


class CarroArriendo(models.Model):
    usuario = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='carro'
    )
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Carro de {self.usuario.username}'


class CarroItem(models.Model):
    carro = models.ForeignKey(
        CarroArriendo, on_delete=models.CASCADE, related_name='items'
    )
    maquinaria = models.ForeignKey(Maquinaria, on_delete=models.CASCADE)
    dias = models.PositiveIntegerField(default=1)

    @property
    def subtotal(self):
        return self.maquinaria.precio_diario * self.dias

    def __str__(self):
        return f'{self.maquinaria.nombre} x {self.dias} días'


class Contrato(models.Model):
    ESTADOS = (
        ('PENDIENTE', 'Pendiente'),
        ('PAGADO', 'Pagado'),
        ('ENTREGADO', 'Entregado'),
        ('COMPLETADO', 'Completado'),
        ('CANCELADO', 'Cancelado'),
    )

    usuario = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='contratos'
    )
    total = models.DecimalField(max_digits=12, decimal_places=2)
    estado = models.CharField(
        max_length=20, choices=ESTADOS, default='PENDIENTE'
    )
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Contrato #{self.id} - {self.usuario.username} ({self.estado})'