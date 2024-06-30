import matplotlib.pyplot as plt
import os
import pandas as pd


# Clase Statistics
class Statistics:
    def __init__(self, sells_data, sales, matches, assistance):
        self.sells_data = sells_data
        self.sales = sales
        self.matches = matches
        self.assistance = assistance
        self.statistics_dir = 'statistics'

    # Método para calcular el promedio de gasto de un cliente VIP
    def calculate_average_spending(self):
        vip_tickets = [ticket for ticket in self.sales.tickets if ticket.ticket_type.lower() == 'vip']
        total_spending = 0
        client_ids = set()

        for ticket in vip_tickets:
            total_spending += ticket.price
            client_ids.add(ticket.client_id)
            client_purchases = [sell for sell in self.sells_data if sell["client_id"] == ticket.client_id]
            for purchase in client_purchases:
                total_spending += purchase["final_price"]

        total_vip_clients = len(client_ids)

        if total_vip_clients > 0:
            average_spending = total_spending / total_vip_clients
        else:
            average_spending = 0
            
        return average_spending

    # Método para calcular la asistencia a los partidos de mayor a menor
    def calculate_match_attendance(self):
        match_attendance = []
        for match in self.matches:
            total_tickets = sum(1 for ticket in self.assistance.tickets if ticket["match_id"] == match.id)
            attended_tickets = sum(1 for ticket in self.assistance.tickets if ticket["match_id"] == match.id and ticket.get("assistance", False))
            attendance_ratio = attended_tickets / total_tickets if total_tickets > 0 else 0
            match_info = {
                "match": f"{match.home_team.name} vs {match.away_team.name}",
                "stadium": match.stadium.name,
                "total_tickets": total_tickets,
                "attended_tickets": attended_tickets,
                "attendance_ratio": attendance_ratio
            }
            match_attendance.append(match_info)
        return sorted(match_attendance, key=lambda x: x["attendance_ratio"], reverse=True)

    # Metodo para obtener el partido con mayor asistencia
    def get_highest_attendance_match(self, match_attendance):
        highest_attendance_match = max(match_attendance, key=lambda x: x["attended_tickets"])
        return highest_attendance_match

    # Metodo para obtener el partido con mayor boletos vendidos
    def get_highest_tickets_sold_match(self, match_attendance):
        highest_tickets_sold_match = max(match_attendance, key=lambda x: x["total_tickets"])
        return highest_tickets_sold_match

    # Método para obtener los 3 productos más vendidos
    def get_top_selling_products(self):
        product_sales = {}
        for sell in self.sells_data:
            product_name = sell["product_name"]
            quantity = sell["quantity"]
            if product_name in product_sales:
                product_sales[product_name] += quantity
            else:
                product_sales[product_name] = quantity
        top_selling_products = sorted(product_sales.items(), key=lambda x: x[1], reverse=True)[:3]
        return top_selling_products

    # Método para obtener los 3 clientes que más compraron boletos
    def get_top_clients(self):
        client_purchases = {}
        for ticket in self.sales.tickets:
            client_id = ticket.client_id
            if client_id in client_purchases:
                client_purchases[client_id] += 1
            else:
                client_purchases[client_id] = 1
        top_clients = sorted(client_purchases.items(), key=lambda x: x[1], reverse=True)[:3]
        return top_clients

    # Metodo para mostrar las estadisticas
    def show_statistics(self):
        # Llama a los metodos para calcular las estadisticas
        average_spending = self.calculate_average_spending()
        match_attendance = self.calculate_match_attendance()
        attendance_table = pd.DataFrame(match_attendance)
        attendance_table = attendance_table.sort_values(by="attendance_ratio", ascending=False)
        highest_attendance_match = self.get_highest_attendance_match(match_attendance)
        highest_tickets_sold_match = self.get_highest_tickets_sold_match(match_attendance)
        top_selling_products = self.get_top_selling_products()
        top_clients = self.get_top_clients()

        print(f"\nPromedio de gasto de un cliente VIP en un partido (ticket + restaurante): ${average_spending:.2f}")
        print("\nTabla de asistencia a los partidos de mejor a peor:\n")
        for match in match_attendance:
            print(f"\nPartido: {match['match']} - Estadio: {match['stadium']} - Boletos vendidos: {match['total_tickets']} - Asistieron: {match['attended_tickets']} - Relación asistencia/venta: {match['attendance_ratio']:.2f}")

        print(f"\nPartido con mayor asistencia: {highest_attendance_match['match']} - Asistieron: {highest_attendance_match['attended_tickets']}")
        print(f"\nPartido con mayor boletos vendidos: {highest_tickets_sold_match['match']} - Boletos vendidos: {highest_tickets_sold_match['total_tickets']}")
        print("\nTop 3 productos más vendidos en el restaurante:")
        for product, quantity in top_selling_products:
            print(f"Producto: {product} - Cantidad vendida: {quantity}")

        print("\nTop 3 clientes (clientes que más compraron boletos):")
        for client_id, purchase_count in top_clients:
            print(f"\nCliente ID: {client_id} - Boletos comprados: {purchase_count}")
        
        # Save attendance table as image
        self.save_table_as_image(attendance_table, 'attendance_table.png', 'Asistencia a los partidos de mejor a peor')

        # Llama al metodo generate_charts para generar los graficos de las estadisticas calculadas
        self.generate_charts(
            average_spending,
            highest_attendance_match,
            highest_tickets_sold_match,
            top_selling_products,
            top_clients,
            match_attendance
        )
    
    # Guardamos la tabla de asistencia a los partidos como imagen
    def save_table_as_image(self, table, filename, title):
        if not os.path.exists(self.statistics_dir):
            os.makedirs(self.statistics_dir)
        fig, ax = plt.subplots(figsize=(10, 6)) 
        ax.axis('tight')
        ax.axis('off')
        ax.table(cellText=table.values, colLabels=table.columns, cellLoc='center', loc='center')
        plt.title(title, y=1.30, pad=-20) 
        plt.tight_layout()
        file_path = os.path.join(self.statistics_dir, filename)
        plt.savefig(file_path)
        plt.close()
        

    # Metodo para generar graficas usando matplotlib
    def generate_charts(self, average_spending, highest_attendance_match, highest_tickets_sold_match, top_selling_products, top_clients, match_attendance):
        # Crear carpeta statistics si no existe
        if not os.path.exists(self.statistics_dir):
            os.makedirs(self.statistics_dir)

        # Gráfico de promedio de gasto
        plt.figure(figsize=(10, 6))
        plt.bar(["Promedio de gasto VIP"], [average_spending], color='blue')
        plt.ylabel('Gasto promedio ($)')
        plt.title('Promedio de gasto de un cliente VIP en un partido')
        plt.savefig(os.path.join(self.statistics_dir, 'average_spending_vip.png'))
        plt.close()

        # Gráfico de partido con mayor asistencia
        plt.figure(figsize=(10, 6))
        plt.bar([highest_attendance_match['match']], [highest_attendance_match['attended_tickets']], color='green')
        plt.ylabel('Cantidad de asistentes')
        plt.title('Partido con mayor asistencia')
        plt.savefig(os.path.join(self.statistics_dir, 'highest_attendance.png'))
        plt.close()

        # Gráfico de partido con mayor boletos vendidos
        plt.figure(figsize=(10, 6))
        plt.bar([highest_tickets_sold_match['match']], [highest_tickets_sold_match['total_tickets']], color='red')
        plt.ylabel('Cantidad de boletos vendidos')
        plt.title('Partido con mayor boletos vendidos')
        plt.savefig(os.path.join(self.statistics_dir, 'highest_tickets_sold.png'))
        plt.close()

        # Gráfico de top 3 productos más vendidos
        product_names, quantities = zip(*top_selling_products)
        plt.figure(figsize=(10, 6))
        plt.bar(product_names, quantities, color='purple')
        plt.ylabel('Cantidad vendida')
        plt.title('Top 3 productos más vendidos en el restaurante')
        plt.savefig(os.path.join(self.statistics_dir, 'top_selling_products.png'))
        plt.close()
        
        # Gráfico de top 3 clientes
        client_ids, purchases = zip(*top_clients)
        client_ids = [str(c) for c in client_ids]
        plt.figure(figsize=(10, 6))
        plt.bar(client_ids, purchases)
        plt.xlabel('ID de clientes')
        plt.ylabel('Boletos comprados')
        plt.title('Top 3 clientes que más compraron boletos')
        plt.savefig(os.path.join('statistics', 'top_clients.png'))
        plt.close()
        
        # Gráfico de asistencia a los partidos
        matches = [match["match"] for match in match_attendance]
        total_tickets = [match["total_tickets"] for match in match_attendance]
        attended_tickets = [match["attended_tickets"] for match in match_attendance]

        x = range(len(matches))
        
        fig, ax = plt.subplots(figsize=(12, 8))
        
        ax.bar(x, total_tickets, width=0.4, label='Boletos Vendidos', align='center')
        ax.bar(x, attended_tickets, width=0.4, label='Asistentes', align='edge')
        
        ax.set_xlabel('Partidos')
        ax.set_ylabel('Cantidad de Boletos')
        ax.set_title('Asistencia a los partidos de mejor a peor')
        ax.set_xticks(x)
        ax.set_xticklabels(matches, rotation=90)
        ax.legend()

        plt.tight_layout()
        plt.savefig(os.path.join(self.statistics_dir, 'attendance_chart.png'))
        plt.close()
        