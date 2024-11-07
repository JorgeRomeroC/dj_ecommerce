from .models import Coupon
class Cart:
    def __init__(self, request):
        self.request = request
        self.session = request.session # Obtenemos la sesión actual
        
        cart = self.session.get('cart') # Obtenemos el carrito de la sesión
        totalAmount = self.session.get('cartTotalAmount')
        if not cart:
            cart = self.session['cart'] = {} # Si no existe el carrito, lo creamos
            totalAmount = self.session['cartTotalAmount'] = 0
            
        self.cart = cart
        self.totalAmount = float(totalAmount)

    def add_to_cart(self, product, quantity):
        """Añadir o actualizar la cantidad de un producto en el carrito"""

        # Si el producto ya está en el carrito, actualiza la cantidad con el valor especificado
        if str(product.id) in self.cart.keys():
            self.cart[str(product.id)]['quantity'] = quantity  # Actualiza con la cantidad especificada
            self.cart[str(product.id)]['subtotal'] = str(float(self.cart[str(product.id)]['price']) * quantity)
        else:
            # Si el producto no está en el carrito, agrégalo con la cantidad especificada
            self.cart[str(product.id)] = {
                'product_id': product.id,
                'name': product.name,
                'price': str(product.price),
                'quantity': quantity,
                'image': product.image.url,
                'category': product.category.name,
                'subtotal': str(product.price * quantity)
            }

        self.save_cart()  # Guarda el carrito actualizado

    def get_products(self):
        products = []
        for key, item in self.cart.items():
            products.append({
                'product_id': item['product_id'],
                'name': item['name'],
                'price': float(item['price']),
                'quantity': int(item['quantity']),
                'subtotal': float(item['subtotal']),
                'image': item['image'],
                'category': item['category']
            })
        return products
        
    def delete_from_cart(self,product):
        """Eliminar del carrito"""
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save_cart()

    def clear(self):
        """Limpiar el carrito"""
        self.session['cart'] = {}
        self.session['cartTotalAmount'] = 0
        # Eliminar el código de cupón de la sesión al limpiar el carrito
        if 'coupon_code' in self.session:
            del self.session['coupon_code']
        self.session.modified = True

    
    
    def save_cart(self):
        """Guardar el carrito"""
        totalAmount = 0
        for key, value in self.cart.items():
            totalAmount += float(value['subtotal'])

        self.session['cartTotalAmount'] = totalAmount
        self.session['cart'] = self.cart
        self.session.modified = True



    def apply_coupon(self, code):
        """Aplicar un cupón de descuento solo una vez"""
        # Verifica si el cupón ya ha sido aplicado
        if self.session.get('coupon_code') == code:
            # Si el cupón ya está en la sesión, devuelve False para indicar que ya fue aplicado
            return False

        try:
            coupon = Coupon.objects.get(code=code, active=True)
            discount = coupon.discount
            # Aplica el descuento al total
            self.totalAmount -= (self.totalAmount * (discount / 100))

            # Guarda el total actualizado en la sesión
            self.session['cartTotalAmount'] = self.totalAmount
            self.session['coupon_code'] = code  # Guarda el código de cupón en la sesión para indicar que fue usado
            self.session.modified = True
            return True
        except Coupon.DoesNotExist:
            # Si el cupón no existe o no está activo
            return False