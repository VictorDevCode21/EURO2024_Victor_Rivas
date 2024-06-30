from .product import Product


# Clase Restaurant
class Restaurant:
    def __init__(self):
        self.products = []

    # Método para cargar los productos desde el archivo de stadiums.txt
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
    
    # Método para obtener la información de los productos
    def get_info(self):
        return self.products

    # Método para buscar productos por nombre
    def search_by_name(self, name):
        return [product for product in self.products if name.lower() in product.name.lower()]

    # Método para buscar productos por tipo
    def search_by_type(self, product_type):
        return [product for product in self.products if product.product_type == product_type]

    # Método para buscar productos en un rango de precio especifico
    def search_by_price_range(self, min_price, max_price):
        return [product for product in self.products if min_price <= product.price <= max_price]
    
    # Metodo para retornar la informacion de los productos en formato de string
    def __str__(self):
        return self.get_info()
    
    # Metodo para retornar la informacion de los productos usando la representacion de string
    def __repr__(self):
        return self.get_info()
    