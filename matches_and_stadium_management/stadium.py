import typing

class Stadium:
    def __init__(self, id: str, name: str, city: str, capacity: int):
        self.id = id 
        self.name = name
        self.city = city
        self.capacity = capacity
        
    def get_info(self):
        return f'The name of the stadium is {self.name}, the id is: {self.id}, the location is: {self.city}, and the capacity is {self.capacity[0]} for General and {self.capacity[1]} for VIP '
    
    def __str__(self):
        return self.get_info()

    def __repr__(self):
        return self.__str__()