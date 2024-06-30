import os
import matplotlib.pyplot as plt

class Statistics:
    def __init__(self, sells_data, sales, matches, assistance):
        self.sells_data = sells_data
        self.sales = sales
        self.matches = matches
        self.assistance = assistance
        self.statistics_dir = os.path.join(os.path.dirname(__file__), '..', 'statistics')

        # Create the statistics directory if it doesn't exist
        if not os.path.exists(self.statistics_dir):
            os.makedirs(self.statistics_dir)

    def calculate_average_spending(self):
        vip_tickets = [ticket for ticket in self.sales.tickets if ticket.ticket_type == "vip"]
        total_spending = 0
        total_clients = len(vip_tickets)

        for ticket in vip_tickets:
            client_spending = sum(
                sale["final_price"]
                for sale in self.sells_data
                if sale["client_id"] == ticket.client_id
            )
            total_spending += client_spending + ticket.price  # Incluimos el precio del ticket

        if total_clients > 0:
            return total_spending / total_clients
        return 0

    def calculate_match_attendance(self):
        match_attendance = []
        for match in self.matches:
            total_tickets = sum(
                1 for ticket in self.assistance.tickets if ticket.get('match_id') == match.id
            )
            attended = sum(
                1 for ticket in self.assistance.tickets if ticket.get('match_id') == match.id and ticket.get('assistance')
            )
            if total_tickets > 0:
                attendance_ratio = attended / total_tickets
            else:
                attendance_ratio = 0
            match_attendance.append({
                "match": f"{match.home_team.name} vs {match.away_team.name}",
                "stadium": match.stadium.name,
                "tickets_sold": total_tickets,
                "attended": attended,
                "attendance_ratio": attendance_ratio
            })
        return match_attendance

    def top_selling_products(self):
        product_sales = {}
        for sale in self.sells_data:
            product = sale["product_name"]
            quantity = sale["quantity"]
            if product in product_sales:
                product_sales[product] += quantity
            else:
                product_sales[product] = quantity
        sorted_sales = sorted(product_sales.items(), key=lambda x: x[1], reverse=True)
        return sorted_sales[:3]

    def top_clients(self):
        client_purchases = {}
        for ticket in self.sales.tickets:
            client_id = ticket.client_id
            if client_id in client_purchases:
                client_purchases[client_id] += 1
            else:
                client_purchases[client_id] = 1
        sorted_clients = sorted(client_purchases.items(), key=lambda x: x[1], reverse=True)
        return sorted_clients[:3]

    def show_statistics(self):
        average_spending = self.calculate_average_spending()
        print(f"El promedio de gasto de un cliente VIP en un partido (ticket + restaurante) es: ${average_spending:.2f}")

        match_attendance = self.calculate_match_attendance()
        print("Asistencia a los partidos de mejor a peor:")
        for match in sorted(match_attendance, key=lambda x: x["attendance_ratio"], reverse=True):
            print(
                f"{match['match']} en {match['stadium']}: "
                f"Boletos vendidos: {match['tickets_sold']}, "
                f"Asistieron: {match['attended']}, "
                f"Relación asistencia/venta: {match['attendance_ratio']:.2f}"
            )

        top_selling_products = self.top_selling_products()
        print("Top 3 productos más vendidos en el restaurante:")
        for product, quantity in top_selling_products:
            print(f"Producto: {product}, Cantidad vendida: {quantity}")

        top_clients = self.top_clients()
        print("Top 3 clientes (clientes que más compraron boletos):")
        for client_id, purchases in top_clients:
            print(f"Cliente ID: {client_id}, Boletos comprados: {purchases}")

    def generate_charts(self):
        match_attendance = self.calculate_match_attendance()

        # Chart for match attendance
        plt.figure(figsize=(10, 6))
        matches = [m["match"] for m in match_attendance]
        attendance_ratios = [m["attendance_ratio"] for m in match_attendance]
        plt.bar(matches, attendance_ratios)
        plt.xlabel('Partidos')
        plt.ylabel('Relación asistencia/venta')
        plt.title('Relación asistencia/venta por partido')
        plt.xticks(rotation=90)
        attendance_chart_path = os.path.join(self.statistics_dir, 'attendance_chart.png')
        plt.savefig(attendance_chart_path)
        plt.close()

        # Chart for top selling products
        top_selling_products = self.top_selling_products()
        plt.figure(figsize=(10, 6))
        products = [p[0] for p in top_selling_products]
        quantities = [p[1] for p in top_selling_products]
        plt.bar(products, quantities)
        plt.xlabel('Productos')
        plt.ylabel('Cantidad vendida')
        plt.title('Top 3 productos más vendidos')
        plt.xticks(rotation=90)
        products_chart_path = os.path.join(self.statistics_dir, 'products_chart.png')
        plt.savefig(products_chart_path)
        plt.close()

        # Chart for top clients
        top_clients = self.top_clients()
        plt.figure(figsize=(10, 6))
        client_ids = [str(c[0]) for c in top_clients]
        purchases = [c[1] for c in top_clients]
        plt.bar(client_ids, purchases)
        plt.xlabel('ID de clientes')
        plt.ylabel('Boletos comprados')
        plt.title('Top 3 clientes que más compraron boletos')
        clients_chart_path = os.path.join(self.statistics_dir, 'clients_chart.png')
        plt.savefig(clients_chart_path)
        plt.close()
