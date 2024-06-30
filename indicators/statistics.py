import matplotlib.pyplot as plt

import matplotlib.pyplot as plt
from typing import List

from matches_and_stadium_management.match import Match
from tickets_and_sales_management.sales import Sales
from assistance_management.assistance import Assistance

class Statistics:
    def __init__(self, sells_data, sales: Sales, matches: List[Match], assistance: Assistance):
        self.sells_data = sells_data
        self.sales = sales
        self.matches = matches
        self.assistance = assistance

    def calculate_vip_average_spend(self):
        vip_clients = [ticket.client_id for ticket in self.sales.tickets if ticket.ticket_type == 'vip']
        vip_spends = {client_id: 0 for client_id in vip_clients}
        
        for sell in self.sells_data:
            client_id = sell['client_id']
            if client_id in vip_spends:
                vip_spends[client_id] += sell['final_price']
        
        vip_ticket_prices = {ticket.client_id: ticket.price for ticket in self.sales.tickets if ticket.ticket_type == 'vip'}
        
        total_spend = 0
        for client_id in vip_spends:
            total_spend += vip_spends[client_id] + vip_ticket_prices.get(client_id, 0)
        
        average_spend = total_spend / len(vip_clients) if vip_clients else 0
        return average_spend

    def calculate_match_attendance(self):
        match_attendance = []
        for match in self.matches:
            total_tickets = sum(1 for ticket in self.assistance.tickets if ticket.match_id == match.id)
            attended_tickets = sum(1 for ticket in self.assistance.tickets if ticket.match_id == match.id and ticket.attended)
            attendance_ratio = attended_tickets / total_tickets if total_tickets else 0
            match_attendance.append({
                'match': f"{match.home_team.name} vs {match.away_team.name}",
                'stadium': match.stadium.name,
                'total_tickets': total_tickets,
                'attended': attended_tickets,
                'attendance_ratio': attendance_ratio
            })
        return sorted(match_attendance, key=lambda x: x['attendance_ratio'], reverse=True)

    def get_top_match(self, key):
        match_stats = self.calculate_match_attendance()
        return max(match_stats, key=lambda x: x[key])

    def get_top_products(self, top_n=3):
        product_sales = {}
        for sell in self.sells_data:
            product_name = sell['product_name']
            quantity = sell['quantity']
            if product_name in product_sales:
                product_sales[product_name] += quantity
            else:
                product_sales[product_name] = quantity
        return sorted(product_sales.items(), key=lambda x: x[1], reverse=True)[:top_n]

    def get_top_clients(self, top_n=3):
        client_tickets = {}
        for ticket in self.sales.tickets:
            client_id = ticket.client_id
            if client_id in client_tickets:
                client_tickets[client_id] += 1
            else:
                client_tickets[client_id] = 1
        return sorted(client_tickets.items(), key=lambda x: x[1], reverse=True)[:top_n]

    def show_statistics(self):
        average_spend = self.calculate_vip_average_spend()
        match_attendance = self.calculate_match_attendance()
        top_match_attendance = self.get_top_match('attended')
        top_match_sales = self.get_top_match('total_tickets')
        top_products = self.get_top_products()
        top_clients = self.get_top_clients()

        print(f"1. Promedio de gasto de un cliente VIP en un partido (ticket + restaurante): {average_spend:.2f}")
        print("\n2. Tabla con la asistencia a los partidos de mejor a peor:")
        for match in match_attendance:
            print(f"Partido: {match['match']}, Estadio: {match['stadium']}, Boletos Vendidos: {match['total_tickets']}, Asistieron: {match['attended']}, Relación Asistencia/Venta: {match['attendance_ratio']:.2f}")
        
        print(f"\n3. Partido con mayor asistencia: {top_match_attendance['match']} en {top_match_attendance['stadium']} con {top_match_attendance['attended']} asistentes.")
        print(f"4. Partido con mayor boletos vendidos: {top_match_sales['match']} en {top_match_sales['stadium']} con {top_match_sales['total_tickets']} boletos vendidos.")
        print("\n5. Top 3 productos más vendidos en el restaurante:")
        for product, quantity in top_products:
            print(f"Producto: {product}, Cantidad Vendida: {quantity}")
        print("\n6. Top 3 clientes (clientes que más compraron boletos):")
        for client_id, tickets in top_clients:
            print(f"Cliente ID: {client_id}, Boletos Comprados: {tickets}")

    def generate_charts(self):
        # Promedio de gasto de un cliente VIP
        average_spend = self.calculate_vip_average_spend()
        plt.figure()
        plt.bar(['Promedio de gasto VIP'], [average_spend])
        plt.title('Promedio de gasto de un cliente VIP en un partido (ticket + restaurante)')
        plt.ylabel('Gasto promedio')
        plt.show()

        # Asistencia a los partidos
        match_attendance = self.calculate_match_attendance()
        matches_names = [match['match'] for match in match_attendance]
        attendance_ratios = [match['attendance_ratio'] for match in match_attendance]
        plt.figure()
        plt.barh(matches_names, attendance_ratios)
        plt.title('Relación Asistencia/Venta de Partidos')
        plt.xlabel('Relación Asistencia/Venta')
        plt.ylabel('Partidos')
        plt.show()

        # Top 3 productos más vendidos en el restaurante
        top_products = self.get_top_products()
        products_names = [product[0] for product in top_products]
        products_quantities = [product[1] for product in top_products]
        plt.figure()
        plt.bar(products_names, products_quantities)
        plt.title('Top 3 productos más vendidos en el restaurante')
        plt.xlabel('Productos')
        plt.ylabel('Cantidad Vendida')
        plt.show()

        # Top 3 clientes (clientes que más compraron boletos)
        top_clients = self.get_top_clients()
        clients_ids = [str(client[0]) for client in top_clients]
        clients_tickets = [client[1] for client in top_clients]
        plt.figure()
        plt.bar(clients_ids, clients_tickets)
        plt.title('Top 3 clientes (clientes que más compraron boletos)')
        plt.xlabel('ID de Cliente')
        plt.ylabel('Boletos Comprados')
        plt.show()