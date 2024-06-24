import typing

class Stadium:
    def __init__(self, id: str, name: str, city: str, capacity: int):
        self.id = id 
        self.name = name
        self.city = city
        self.capacity = capacity
        self.seats = {'General': [], 'VIP': []}
        self.booked_seats = {"General": [], "VIP": []}
        
    def set_seats(self, general_capacity: list, vip_capacity: list):
        self.general_seats = [f"G{i}" for i in range(1, general_capacity + 1)]
        self.vip_seats = [f"V{i}" for i in range(1, vip_capacity + 1)]
        
    def get_available_seats(self, ticket_type):
        if ticket_type.lower() == "general":
            return [seat for seat in self.general_seats if seat not in self.booked_seats["General"]]
        elif ticket_type.lower() == "vip":
            return [seat for seat in self.vip_seats if seat not in self.booked_seats["VIP"]]
        else:
            return []
        
    def book_seat(self, ticket_type, seat):
        if ticket_type.lower() == "general" and seat in self.general_seats and seat not in self.booked_seats["General"]:
            self.booked_seats["General"].append(seat)
            return True
        elif ticket_type.lower() == "vip" and seat in self.vip_seats and seat not in self.booked_seats["VIP"]:
            self.booked_seats["VIP"].append(seat)
            return True
        else:
            return False
        
    def get_info(self):
        return f'{self.name}, the location of the stadium is: {self.city}, and the capacity is {self.capacity[0]} for General and {self.capacity[1]} for VIP '
    
    def __str__(self):
        return self.get_info()

    def __repr__(self):
        return self.__str__()