import typing 


# Definicion de la clase Client
class Client:
    def __init__(self, name: str, id: int, age: int):
        self.name = name
        self.id = id
        self.age = age
        
    # Metodo para obtener la informacion del cliente
    def get_info(self):
        return f"Cliente: {self.name} - Cedula: {self.id} - Edad: {self.age}"

    # Metodo para transformar la informacion del cliente de objeto a string
    def __str__(self):
        return self.get_info()
    
    # Metodo para retornar un string imprimible con la informacion del cliente
    def __repr__(self):
        return self.get_info()

