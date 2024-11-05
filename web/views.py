from django.shortcuts import render, get_object_or_404, redirect

from web.cart import Cart
from web.models import *

def index(request):
    list_products = Product.objects.all()
    list_categories = Category.objects.all()
    context = {
        'products': list_products,
        'categories': list_categories,
    }
    return render(request, 'index.html', context)


def product_per_category(request, category_id):
    """Vista de productos por categoría"""
    objCategory = get_object_or_404(Category, pk=category_id)
    list_products = objCategory.product_set.all()

    list_categories = Category.objects.all()
    context = {
        'products': list_products,
        'categories': list_categories,
        'current_category': objCategory,  # Opcional, para mostrar la categoría actual
    }
    return render(request, 'index.html', context)


def product_per_name(request):
    """Vista para filtrar productos por nombre"""
    name = request.POST['name']
    
    list_products = Product.objects.filter(name__contains=name)
    list_categories = Category.objects.all()
    
    context = {
        'catergories': list_categories,
        'products' : list_products
    }
    return render(request, 'index.html', context)


def product_detail(request, product_id):
    """Vista para mostrar detalle de un producto"""
    objProduct = get_object_or_404(Product, pk=product_id)
    context = {
        'product': objProduct
    }
    return render(request, 'producto.html', context)


def cart(request):
    return render(request, 'carrito.html')


def add_cart(request, product_id):
    """Vista para añadir un producto al carrito"""
    if request.method == 'POST':
        # Intenta obtener 'quantity' y usa 1 como valor por defecto si no está presente
        quantity = int(request.POST.get('quantity', 1))
    else:
        quantity = 1

    objProduct = Product.objects.get(pk=product_id)  # Obtenemos el producto
    cartProduct = Cart(request)  # Creamos una instancia del carrito
    cartProduct.add_to_cart(objProduct, quantity)  # Añadimos el producto al carrito

    if request.method == 'POST':
        return redirect('/')

    return render(request, 'carrito.html')


def delete_cart(request, product_id):
    """Vista para eliminar un producto del carrito"""
    objProduct = Product.objects.get(pk=product_id)  # Obtenemos el producto
    cartProduct = Cart(request)  # Creamos una instancia del carrito
    cartProduct.delete_from_cart(objProduct)  # Eliminamos el producto del carrito

    return render(request, 'carrito.html')


def clear_cart(request):
    """Vista para limpiar el carrito"""
    cartProduct = Cart(request)  # Creamos una instancia del carrito
    cartProduct.clear()  # Limpiamos el carrito

    return render(request, 'carrito.html')