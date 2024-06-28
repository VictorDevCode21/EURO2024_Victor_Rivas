from .product import Product

class Restaurant:
    def __init__(self):
        self.products = []

    def load_products(self, stadium_data):
        if stadium_data:
            for stadium in stadium_data:
                if "restaurants" in stadium:
                    for restaurant in stadium["restaurants"]:
                        if "products" in restaurant:
                            for product_data in restaurant["products"]:
                                name = product_data.get('name')
                                additional = product_data.get('adicional')  # Corregir a 'additional'
                                price = float(product_data.get('price')) * 1.16  # Convertir precio a float y añadir IVA
                                stock = product_data.get('stock')
                                category = ''

                                if additional in ['alcoholic', 'non-alcoholic']:
                                    product_type = 'drink'
                                    if additional == 'alcoholic':
                                        category = 'alcoholic'
                                    elif additional == "non-alcoholic":
                                        category = "non-alcoholic"
                                elif additional in ['package', 'plate']:
                                    product_type = 'food'
                                    if additional == 'package':
                                        category = 'package'
                                    elif additional == 'plate':
                                        category = 'plate'
                                else:
                                    continue  # Ignorar productos desconocidos

                                self.products.append(Product(name, product_type, price, category, stock))
                        else:
                            print(f"No se encontraron productos en el restaurante {restaurant.get('name')}")
                else: 
                    print("No se encontraron restaurantes en el estadio")
        else:
            print("No se encontraron estadios")
                        
    def get_info(self):
        return self.products

    def search_by_name(self, name):
        return [product for product in self.products if name.lower() in product.name.lower()]

    def search_by_type(self, product_type):
        return [product for product in self.products if product.product_type == product_type]

    def search_by_price_range(self, min_price, max_price):
        return [product for product in self.products if min_price <= product.price <= max_price]
    
    def __str__(self):
        return self.get_info()
    
    def __repr__(self):
        return self.get_info()
    