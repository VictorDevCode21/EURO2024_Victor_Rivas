import typing 


class Client:
    def __init__(self, name: str, id: int, age: int):
        self.name = name
        self.id = id
        self.age = age
        
    def get_info(self):
        return f"Cliente: {self.name} - Cedula: {self.id} - Edad: {self.age}"

    def __str__(self):
        return self.get_info()
    
    def __repr__(self):
        return self.get_info()

