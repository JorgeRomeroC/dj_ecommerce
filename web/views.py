from django.shortcuts import render, get_object_or_404

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