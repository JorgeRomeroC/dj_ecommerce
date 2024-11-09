from django.shortcuts import render, get_object_or_404, redirect

from web.cart import Cart
from web.models import *

# views.py
from datetime import datetime
from django.shortcuts import render


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

    # Crear una instancia del carrito
    cart = Cart(request)

    # Obtener la cantidad actual del producto en el carrito, si existe
    quantity = cart.cart.get(str(product_id), {}).get('quantity', 1)  # Por defecto, 1 si no está en el carrito

    context = {
        'product': objProduct,
        'quantity': quantity  # Pasar la cantidad al contexto
    }
    return render(request, 'producto.html', context)



def cart(request):
    cartProduct = Cart(request)

    if request.method == 'POST':
        coupon_code = request.POST.get('coupon')
        if coupon_code:
            success = cartProduct.apply_coupon(coupon_code)
            if success:
                message = "Cupón aplicado exitosamente."
            else:
                message = "El cupón ya fue aplicado o es inválido."
        else:
            message = "Por favor, ingresa un código de cupón."

        return render(request, 'carrito.html', {'message': message, 'cart': cartProduct})

    return render(request, 'carrito.html', {'cart': cartProduct})


def add_cart(request, product_id):
    """Vista para añadir o actualizar un producto en el carrito"""
    if request.method == 'POST':
        # Obtener la cantidad especificada en el formulario
        quantity = int(request.POST.get('quantity', 1))

        objProduct = Product.objects.get(pk=product_id)  # Obtenemos el producto
        cartProduct = Cart(request)  # Creamos una instancia del carrito
        cartProduct.add_to_cart(objProduct, quantity)  # Añadimos o actualizamos el producto en el carrito

        return redirect('web:cart')  # Redirecciona al carrito después de actualizar

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
    # Asegurarnos de eliminar el código de cupón en la sesión
    if 'coupon_code' in request.session:
        del request.session['coupon_code']
    return render(request, 'carrito.html')