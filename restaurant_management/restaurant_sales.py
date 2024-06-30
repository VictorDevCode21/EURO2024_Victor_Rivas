import json
from math import isqrt

# Clase para manejar las ventas del modulo 5 de restaurantes
class RestaurantSales:
    def __init__(self, restaurant, sales):
        self.restaurant = restaurant
        self.sales = sales

    # Método para verificar si un número es perfecto
    def is_perfect_number(self, num):
        sum_divisors = 1
        for i in range(2, isqrt(num) + 1):
            if num % i == 0:
                sum_divisors += i
                if i != num // i:
                    sum_divisors += num // i
        return sum_divisors == num
    
    # Metodo para obtener la información de un cliente
    def get_client_info(self, client_id):
        client = self.sales.clients.get(client_id)
        if not client:
            return "Cliente no encontrado."
        return client.get_info()

    # Metodo para procesar la venta de productos
    def sell_products(self, client_id, product_name, quantity, product_type):
        # Obtener cliente
        client = self.sales.clients.get(client_id)
        if not client:
            return "Cliente no encontrado.", None

        # Verificar tipo de entrada
        client_tickets = [ticket for ticket in self.sales.tickets if ticket.client_id == client_id]
        if not any(ticket.ticket_type.lower() == 'vip' for ticket in client_tickets):
            return "Acceso denegado. Solo clientes VIP pueden realizar compras.", None

        # Verificar parámetros del producto
        if not product_name or quantity <= 0:
            return "No se especificaron productos para comprar o la cantidad es incorrecta.", None
        
        total = 0
        items = []
            
        # Iteramos en productos para encontrar el nombre y tipo del producto y verificar que exista
        product = next((p for p in self.restaurant.products if p.name == product_name and p.product_type == product_type), None)
        
        # Si el producto existe y tiene stock, procesamos la venta
        if product and product.stock >= quantity:
            # Si el cliente es menor de edad y trata de consumir alcohol, se rechaza la venta
            if product.product_type == 'drink' and product.category == 'alcoholic' and client.age < 18:
                return f"No se puede vender bebidas alcohólicas a menores de edad: {product_name}", None
            subtotal = product.price * quantity
            items.append(f"{product.name} x {quantity} - ${subtotal:.2f}")
            total += subtotal
        # Si el producto no se encuentra o no tiene stock, se le indica al cliente
        else:
            return f"Producto no encontrado o sin disponibilidad: {product_name}", None

        # Si la cedula del cliente es un numero perfecto, se le aplica un descuento del 15%
        if self.is_perfect_number(int(client_id)):
            discount = total * 0.15
            total -= discount
        else:
            discount = 0
        
        # Actualizamos el inventario
        updated_product = self.update_inventory(product_name, quantity, product_type)
        
        # Si el inventario se actualiza correctamente, se genera la venta y se manda la informacion a sale_data
        if updated_product:
            sale_data = {
                'client_id': client_id,
                'product_name': product_name,
                'quantity': quantity,
                'total': round(total + discount, 2),
                'discount': round(discount, 2),
                'final_price': round(total, 2)
            }
            return f"Productos seleccionados:\n" + "\n".join(items) + f'\nPrecio del producto: {product.price:.2f}' + f"\nSubtotal: ${total:.2f}\nDescuento: ${discount:.2f}\nTotal: ${total:.2f}\nCompra exitosa.", sale_data
        else:
            return "Error al actualizar el inventario.", None
        
    # Metodo para actualizar el inventario
    def update_inventory(self, product_name, quantity, product_type):
        product = next((p for p in self.restaurant.products if p.name == product_name and p.product_type == product_type), None)
        if product:
            product.stock -= quantity
            return product
        return None