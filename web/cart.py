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
        """Añadir al carrito"""

        if str(product.id) not in self.cart.keys():
            self.cart[product.id] = {
                'product_id': product.id,
                'name': product.name,
                'price': str(product.price),
                'quantity': quantity,
                'image': product.image.url,
                'category': product.category.name,
                'subtotal':str(product.price * quantity)
            }
        else:
            for key, value in self.cart.items():
                if key == str(product.id):
                    value['quantity'] = int(value['quantity']) + quantity
                    value['subtotal'] = str(float(value['price']) * value['quantity'])
                    break
        self.save_cart()

        
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

    
    
    def save_cart(self):
        """Guardar el carrito"""
        totalAmount = 0
        for key, value in self.cart.items():
            totalAmount += float(value['subtotal'])

        self.session['cartTotalAmount'] = totalAmount
        self.session['cart'] = self.cart
        self.session.modified = True
        