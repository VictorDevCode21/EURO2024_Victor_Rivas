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

    # Definimos un metodo para agregar clientes
    def add_client(self, name: str, id: int, age: int):
        if id not in self.clients:
            self.clients[id] = Client(name, id, age)
        else:
            print(f"Client with ID {id} already exists.")

    # Definimos un metodo para agregar tickets
    def add_ticket(self, client_id: int, match_id: str, ticket_type: str, seat: str):
        if client_id in self.clients:
            ticket = Ticket(client_id, match_id, ticket_type, seat)
            self.tickets.append(ticket)
        else:
            print(f"No client found with ID {client_id}")

    # Definimos un metodo para obtener la informacion de un cliente
    def get_client_info(self, client_id: int):
        if client_id in self.clients:
            return self.clients[client_id].get_info()
        else:
            return "Client not found"

    # Definimos un metodo para obtener la informacion del boleto
    def get_ticket_info(self, client_id: int):
        return [ticket.get_info() for ticket in self.tickets if ticket.client_id == client_id]

    # Definimos un metodo estatico para verificar si un numero es un numero vampiro
    @staticmethod
    def is_vampire_number(number: int) -> bool:
        digits = sorted(str(number))
        length = len(digits)

        # Debe tener un número par de dígitos
        if length % 2 != 0:
            return False

        # Probar todas las posibles combinaciones de factores
        half_length = length // 2
        for i in range(10**(half_length - 1), 10**half_length):
            for j in range(i, 10**half_length):
                if i * j == number:
                    product_digits = sorted(str(i) + str(j))
                    if product_digits == digits:
                        # Asegurarse de que no ambos terminan en cero
                        if not (str(i).endswith('0') and str(j).endswith('0')):
                            return True
        return False
    
    # Definimos un metodo para pedir los datos al usuario
    def get_user_input(self, matches):
        # Pedimos los datos
        name = input("Ingrese el nombre del cliente: ")
        id = int(input("Ingrese la cédula del cliente: "))
        age = int(input("Ingrese la edad del cliente: "))

        print("\nPartidos disponibles:")
        # Muestramos la lista de partidos junto con su informacion accediendo al metodo de match
        for i, match in enumerate(matches):
            print(f"{i + 1}. {match.get_info()}")

        # Le pedimos al usuario que seleccione un partido
        match_index = int(input("Seleccione el partido (número): ")) - 1
        
        # Guardamos el partido que selecciono
        selected_match = matches[match_index]

        # Le pedimos al usuario que seleccione el tipo de entrada
        ticket_type = input("Tipo de entrada (General/VIP): ").lower()
        
        # Seteamos los asientos reservados para el estadio del partido seleccionado
        selected_match.stadium.set_booked_seats('data/tickets.txt', selected_match.id)
        
        # Obtenemos los asientos disponibles para el tipo de entrada seleccionado
        available_seats = selected_match.stadium.get_available_seats(ticket_type)
        
        # Mostramos al usuario los asientos disponibles y los que ya estan reservados
        print("\nAsientos disponibles:\n")
        print(available_seats)
        
        print("Asientos no disponibles:\n")
        print(selected_match.stadium.booked_seats[ticket_type])
        
        # Pedimos al usuario que seleccione un asiento
        seat_number = input("Seleccione su asiento: (G/V seguido del numero de asiento) ").upper()
        
        # Si el asiento que selecciono no esta disponible, le pedimos que seleccione otro asiento
        while seat_number not in available_seats:
            print("El número del asiento no es válido o el asiento ya está reservado. Por favor, seleccione otro asiento.")
            seat_number = input("Seleccione su asiento: (G/V seguido del numero de asiento)").upper()
        seat = seat_number

        # Le mostramos el asiento al usuario
        print(f"Selected seat: {seat}")
        return name, id, age,selected_match , selected_match.id, ticket_type, seat

    # Procesamos el ticket obteniendo la informacion previamente pedida al usuario
    def process_ticket_sale(self, matches):
        name, id, age, selected_match, selected_match.id, ticket_type, seat = self.get_user_input(matches)

        # Agregamos el cliente y el ticket
        self.add_client(name, id, age)
        self.add_ticket(id, selected_match.id, ticket_type, seat)

        # Calculamos el precio del ticket
        ticket_price = 35 if ticket_type.lower() == 'general' else 75

        # Calculamos el descuento dependiendo de si la cedula del cliente es un numero vampiro
        discount = 0.5 if self.is_vampire_number(id) else 0

        # Calculamos el subtotal, iva y total
        subtotal = ticket_price * (1 - discount)
        iva = subtotal * 0.16
        total = subtotal + iva

        # Mostramos la informacion del ticket al usuario 
        print(f"\nInformación del ticket:")
        print(f"Asiento: {seat}")
        print(f"Subtotal: ${subtotal:.2f}")
        print(f"Descuento: ${subtotal * discount:.2f}")
        print(f"IVA: ${iva:.2f}")
        print(f"Total: ${total:.2f}")

        # Le preguntamos al usuario si desea proceder con el pago
        confirm = input("¿Desea proceder con el pago? (si/no): ")
        
        # Si confirma, procesamos la compra, de lo contrario, la cancelamos.
        if confirm.lower() == 'si':
            print("Pago exitoso. ¡Gracias por su compra! \n")
        else:
            print("La compra ha sido cancelada.\n")
