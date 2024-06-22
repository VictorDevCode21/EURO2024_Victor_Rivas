import typing

class Stadium:
    def __init__(self, name, location):
        self.name = name 
        self.location = location 
        
    def get_info(self):
        return f'The name of the stadium is {self.name} and the location is: {self.location}'
    
