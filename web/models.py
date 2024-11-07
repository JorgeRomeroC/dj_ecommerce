from django.db import models


class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount = models.FloatField()  # Porcentaje de descuento, ej. 10 para 10%
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.code} - {self.discount}%"

class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name='Nombre Categoria')
    register_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        
        
class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.RESTRICT)
    name = models.CharField(max_length=200, verbose_name='Nombre de Producto')
    description = models.TextField(null=True)
    price = models.DecimalField(max_digits=9, decimal_places=0)
    register_date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='products',blank=True)
    
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
    