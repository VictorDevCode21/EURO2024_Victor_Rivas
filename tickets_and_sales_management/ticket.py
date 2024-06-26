from datetime import datetime as date


# Definicion de la clase Ticket
class Ticket:
    def __init__(self, client_id: int, match_id: str, ticket_type: str, seat: str):
        self.client_id = client_id
        self.match_id = match_id
        self.ticket_type = ticket_type
        self.seat = seat
        self.price = 35 if ticket_type == "General" else 75
        self.purchase_date = date.now()

    # Metodo para obtener la informacion del boleto
    def get_info(self):
        return (
            f"Cedula: {self.client_id}, ID Del partido: {self.match_id}, "
            f"Tipo de entrada: {self.ticket_type}, Asiento: {self.seat}, "
            f"Precio: {self.price}, Dia de compra: {self.purchase_date}"
        )

    # Metodo para transformar la informacion del boleto de objeto a diccionario
    def to_dict(self):
        return {
            "client_id": self.client_id,
            "match_id": self.match_id,
            "ticket_type": self.ticket_type,
            "seat": self.seat,
        }

    # Metodo para transformar la informacion del boleto de objeto a string
    def __str__(self):
        return self.get_info()

    # Metodo para retornar un string imprimible con la informacion del boleto
    def __repr__(self):
        return self.get_info()
