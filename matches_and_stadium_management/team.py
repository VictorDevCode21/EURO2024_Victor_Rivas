import typing


class Team:
    def __init__(self, id: int, code: str, name: str, group: str):
        self.id = id
        self.code = code
        self.name = name 
        self.group = group 
        
    def get_info(self):
        return f"Team: {self.name}  Code: ({self.code}) - Group: {self.group}"
    
    def __str__(self):
        return self.get_info()
    
    def __repr__(self):
        return self.__str__()