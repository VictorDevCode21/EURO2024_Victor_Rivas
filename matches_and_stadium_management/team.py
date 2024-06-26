import typing

# Definicion de la clase Team
class Team:
    def __init__(self, id: int, code: str, name: str, group: str):
        self.id = id
        self.code = code
        self.name = name 
        self.group = group 
        
    # Metodo para obtener la informacion del equipo/pais
    def get_info(self):
        return f"Team: {self.name}  Code: ({self.code}) - Group: {self.group}"
    
    # Metodo para retornar la informacion en formato string 
    def __str__(self):
        return self.get_info()
    
    # Metodo para retornar un string imprimible con la informacion del equipo/pais
    def __repr__(self):
        return self.__str__()