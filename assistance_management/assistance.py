import typing
import json


# Definicion de la clase Assistance
class Assistance: 
    def __init__(self):
        self.tickets = []
        
    # Cargamos los datos de tickets en la lista self.tickets
    def load_data(self, tickets_data):
        if tickets_data:
            for ticket in tickets_data:
                self.tickets.append(ticket)
    
    # Validamos si el ticket es valido y si ya ha sido utilizado
    def validate_authenticity(self, ticket_id: str):
        ticket_found = False
        for ticket in self.tickets:
            if ticket.get('ticket_id') == ticket_id:
                ticket_found = True
                if not ticket.get('assistance', False):
                    ticket['assistance'] = True
                    return True, "El ticket es válido y la asistencia ha sido registrada."
                else:
                    return False, "El ticket ya ha sido utilizado."
        
        if not ticket_found:
            return False, "El ticket es falso o no existe en el sistema."

    # Guardamos los datos actualizados en el archivo
    def save_data(self, file_path):
        with open(file_path, 'w') as file:
            json.dump(self.tickets, file, indent=4)