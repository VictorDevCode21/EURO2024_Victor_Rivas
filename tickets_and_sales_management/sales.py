# Importamos las librerias necesarias y archivos 
from .client import Client
from .ticket import Ticket
import json 
import os 



# Definimos la clase Sales
class Sales:
    def __init__(self):
        self.clients = {}
        self.tickets = []

    # Cargamos los datos para posteriormente trabajar con ellos
    def load_data(self, clients_data, tickets_data):

        # Si hay data de clientes recorremos los clients_data y los guardamos en el diccionario clients
        if clients_data:
            for client in clients_data:
                self.clients[client['id']] = Client(client['name'], client['id'], client['age'])

        # Si hay data de tickets recorremos los tickets_data y los guardamos en la lista tickets
        if tickets_data:
            for ticket in tickets_data:
                self.tickets.append(Ticket(ticket['client_id'], ticket['match_id'], ticket['ticket_type'], ticket['seat']))

    # Definimos una funcion para agregar clientes
    def add_client(self, name: str, id: int, age: int):
        if id not in self.clients:
            self.clients[id] = Client(name, id, age)
        else:
            print(f"Client with ID {id} already exists.")

    # Definimos una funcion para agregar tickets
    def add_ticket(self, client_id: int, match_id: str, ticket_type: str, seat: str):
        if client_id in self.clients:
            ticket = Ticket(client_id, match_id, ticket_type, seat)
            self.tickets.append(ticket)
        else:
            print(f"No client found with ID {client_id}")

    # Definimos una funcion para obtener la informacion de un cliente
    def get_client_info(self, client_id: int):
        if client_id in self.clients:
            return self.clients[client_id].get_info()
        else:
            return "Client not found"

    def get_ticket_info(self, client_id: int):
        return [ticket.get_info() for ticket in self.tickets if ticket.client_id == client_id]

    @staticmethod
    def is_vampire_number(number: int) -> bool:
        digits = sorted(str(number))
        for i in range(1, len(digits)):
            left, right = int("".join(digits[:i])), int("".join(digits[i:]))
            if left * right == number and str(left) + str(right) == str(number):
                return True
        return False
    
    def get_user_input(self, matches):
        name = input("Ingrese el nombre del cliente: ")
        id = int(input("Ingrese la cédula del cliente: "))
        age = int(input("Ingrese la edad del cliente: "))

        print("\nPartidos disponibles:")
        for i, match in enumerate(matches):
            print(f"{i + 1}. {match.get_info()}")

        match_index = int(input("Seleccione el partido (número): ")) - 1
        selected_match = matches[match_index]

        ticket_type = input("Tipo de entrada (General/VIP): ")
        
        available_seats = selected_match.stadium.get_available_seats(ticket_type)
        print("\nAsientos disponibles:\n")
        print(available_seats)
        
        seat = input("Seleccione su asiento: ")
        while seat not in available_seats:
            print("El asiento no está disponible. Por favor, seleccione otro asiento.")
            seat = input("Seleccione su asiento: ")
        

        return name, id, age, selected_match.id, ticket_type, seat

    def process_ticket_sale(self, matches):
        name, id, age, match, match_id, ticket_type, seat = self.get_user_input(matches)

        self.add_client(name, id, age)
        self.add_ticket(id, match_id, ticket_type, seat)

        ticket_price = 35 if ticket_type.lower() == 'general' else 75

        discount = 0.5 if self.is_vampire_number(int(id)) else 0

        subtotal = ticket_price * (1 - discount)
        iva = subtotal * 0.16
        total = subtotal + iva

        print(f"\nInformación del ticket:")
        print(f"Asiento: {seat}")
        print(f"Subtotal: ${subtotal:.2f}")
        print(f"Descuento: ${subtotal * discount:.2f}")
        print(f"IVA: ${iva:.2f}")
        print(f"Total: ${total:.2f}")

        confirm = input("¿Desea proceder con el pago? (sí/no): ")
        if confirm.lower() == 'sí':
            match.stadium.book_seat(ticket_type, seat)
            print("Pago exitoso. ¡Gracias por su compra!")
        else:
            print("La compra ha sido cancelada.")
