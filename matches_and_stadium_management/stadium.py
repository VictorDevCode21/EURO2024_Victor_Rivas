import typing
import json


#Definimos la clase Stadium
class Stadium:
    def __init__(self, id: str, name: str, city: str, capacity: int):
        self.id = id 
        self.name = name
        self.city = city
        self.capacity = capacity
        self.seats = {'General': [], 'VIP': []}
        self.booked_seats = {"general": [], "vip": []}
        
    # Definimos un metodo para buscar los asientos 
    def set_seats(self, general_capacity: list, vip_capacity: list):
        self.general_seats = [f"G{i}" for i in range(1, general_capacity + 1)]
        self.vip_seats = [f"V{i}" for i in range(1, vip_capacity + 1)]
        
    # Definimos un metodo para cargar los asientos reservados del archivo de tickets
    def set_booked_seats(self, tickets_file_path, match_id):
        try:
            with open(tickets_file_path, 'r') as file:
                tickets = json.load(file)
                for ticket in tickets:
                    if ticket['match_id'] == match_id:
                        ticket_type = ticket['ticket_type'].lower()
                        seat = ticket['seat']
                        if ticket_type == "general":
                            if seat not in self.booked_seats["general"]:
                                self.booked_seats["general"].append(seat)
                        elif ticket_type == "vip":
                            if seat not in self.booked_seats["vip"]:
                                self.booked_seats["vip"].append(seat)
        except FileNotFoundError:
            print(f"El archivo {tickets_file_path} no se encontró.")
        except json.JSONDecodeError:
            print("Error al decodificar el archivo JSON.")
        
    # Metodo para obtener los asientos disponibles
    def get_available_seats(self, ticket_type):
        if ticket_type.lower() == "general":
            return [seat for seat in self.general_seats if seat not in self.booked_seats["general"]]
        elif ticket_type.lower() == "vip":
            return [seat for seat in self.vip_seats if seat not in self.booked_seats["vip"]]
        else:
            return []
        
    # Metodo para reservar un asiento
    def book_seat(self, ticket_type, seat):
        if ticket_type.lower() == "general" and seat in self.general_seats and seat not in self.booked_seats["general"]:
            self.booked_seats["general"].append(seat)
            return True
        elif ticket_type.lower() == "vip" and seat in self.vip_seats and seat not in self.booked_seats["vip"]:
            self.booked_seats["vip"].append(seat)
            return True
        else:
            return False
        
    # Metodo para obtener la informacion del estadio
    def get_info(self):
        return f'{self.name}, the location of the stadium is: {self.city}, and the capacity is {self.capacity[0]} for General and {self.capacity[1]} for VIP '
    
    # Metodo str para obtener la informacion del estadio en forma de string
    def __str__(self):
        return self.get_info()

    # Metodo repr para obtener la informacion del estadio en forma de string
    def __repr__(self):
        return self.__str__()