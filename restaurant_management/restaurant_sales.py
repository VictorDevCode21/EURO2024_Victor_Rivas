import json
from math import isqrt

class RestaurantSales:
    def __init__(self, restaurant, sales):
        self.restaurant = restaurant
        self.sales = sales

    def is_perfect_number(self, num):
        sum_divisors = 1
        for i in range(2, isqrt(num) + 1):
            if num % i == 0:
                sum_divisors += i
                if i != num // i:
                    sum_divisors += num // i
        return sum_divisors == num
    
    def get_client_info(self, client_id):
        client = self.sales.tickets.get(client_id)
        print("client", client)
        if not client:
            return "Cliente no encontrado."
        return client.get_info()

    def sell_products(self, client_id, product_name, quantity, product_type):
        client = next((ticket for ticket in self.sales.tickets if ticket.client_id == client_id), None)
        if not client:
            return "Cliente no encontrado."
        
        if client.ticket_type != 'vip':
            return "Acceso denegado. Solo clientes VIP pueden realizar compras."

        if not product_name or quantity <= 0:
            return "No se especificaron productos para comprar o la cantidad es incorrecta."
        
        total = 0
        items = []
            
        product = next((p for p in self.restaurant.products if p.name == product_name and p.product_type == product_type), None)
        
        if product and product.stock >= quantity:
            if product.product_type == 'drink' and product.category == 'alcoholic' and client.age < 18:
                return f"No se puede vender bebidas alcohólicas a menores de edad: {product_name}"
            subtotal = product.price * quantity
            items.append(f"{product.name} x {quantity} - ${subtotal:.2f}")
            total += subtotal
        else:
            return f"Producto no encontrado: {product_name}"

        if self.is_perfect_number(int(client_id)):
            discount = total * 0.15
            total -= discount
        else:
            discount = 0
        
        updated_product = self.update_inventory(product_name, quantity, product_type)
        
        if updated_product: return f"Productos seleccionados:\n" + "\n".join(items) + f'\nPrecio del producto: {product.price:.2f}' + f"\nSubtotal: ${total:.2f}\nDescuento: ${discount:.2f}\nTotal: ${total:.2f}\nCompra exitosa."
        else: return "Error al actualizar el inventario."
        
    def update_inventory(self, product_name, quantity, product_type):
        product = next((p for p in self.restaurant.products if p.name == product_name and p.product_type == product_type), None)
        if product:
            product.stock -= quantity
            print(f"Inventario actualizado: {product.name} - {product.stock} unidades")
            return product
        return None 