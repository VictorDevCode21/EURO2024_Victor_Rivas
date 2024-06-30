import typing


# Clase Product
class Product:
    def __init__(self, name: str, product_type: str, price: float, category: str, stock: int):
        self.name = name
        self.product_type = product_type
        self.price = price
        self.category = category
        self.stock = stock
        
    # Metodo para convertir la información del producto en un diccionario
    def to_dict(self):
        return {
            "name": self.name,
            "product_type": self.product_type,
            "price": self.price,
            "category": self.category,
            "stock": self.stock
        }
