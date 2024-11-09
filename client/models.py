from django.db import models
from django.contrib.auth.models import User
from web.models import *


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rut = models.CharField(max_length=10, blank=True)
    sex = models.CharField(max_length=1, default='M',verbose_name='Sexo')
    phone = models.CharField(max_length=15, blank=True, verbose_name='Teléfono')
    date_birth = models.DateField(null=True, blank=True, verbose_name='Fecha de nacimiento')
    address = models.CharField(max_length=255, blank=True, verbose_name='Dirección')
    state = models.CharField(max_length=255, blank=True, verbose_name='Estado')

    def __str__(self):
        return self.rut


class Order(models.Model):

    STATE_CHOICES = (
        ('0', 'En proceso'),
        ('1', 'Enviado'),
        ('2', 'Entregado'),
        ('3', 'pagado'),
        ('4', 'Cancelado'),
    )

    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    date_register = models.DateField(verbose_name='Fecha de registro')
    number_order = models.CharField(max_length=255, verbose_name='Número de orden')
    total = models.DecimalField(max_digits=9, decimal_places=0, default=0, verbose_name='Total')
    state = models.CharField(max_length=255, blank=True, default=0, choices=STATE_CHOICES ,verbose_name='Estado')

    def __str__(self):
        return self.number_order


class details_order(models.Model):
    order = models.ForeignKey(Order, on_delete=models.RESTRICT)
    product = models.ForeignKey(Product, on_delete=models.RESTRICT)
    quantity = models.IntegerField(default=1)
    subtotal = models.DecimalField(max_digits=9, decimal_places=0)

    def __str__(self):
        return self.product.name