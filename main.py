# Importamos las librerias a utilizar
from matches_and_stadium_management.api import API
from matches_and_stadium_management.match import Match
from matches_and_stadium_management.team import Team
from matches_and_stadium_management.stadium import Stadium
from tickets_and_sales_management.sales import Sales
from assistance_management.assistance import Assistance
from restaurant_management.restaurant import Restaurant
from restaurant_management.restaurant_sales import RestaurantSales
from indicators.statistics import Statistics
from data_management import DataManager
from datetime import datetime
import os
from dotenv import load_dotenv
import json

# Cargamos el archivo dotenv
load_dotenv()

data_manager = DataManager()


# Funcion principal del programa
def Main():

    # Cargamos los datos desde el archivo txt
    teams_data = data_manager.load_from_file(data_manager.teams_file)
    stadiums_data = data_manager.load_from_file(data_manager.stadiums_file)
    matches_data = data_manager.load_from_file(data_manager.matches_file)
    clients_data = data_manager.load_from_file(data_manager.clients_file)
    tickets_data = data_manager.load_from_file(data_manager.tickets_file)
    sells_data = data_manager.load_from_file(data_manager.sells_file)

    # Si no hay datos, los cargamos desde la API y los guardamos en un archivo txt
    if not teams_data or not stadiums_data or not matches_data:
        data_manager.pre_load_data()
        # Cargamos nuevamente los datos
        teams_data = data_manager.load_from_file(data_manager.teams_file)
        stadiums_data = data_manager.load_from_file(data_manager.stadiums_file)
        matches_data = data_manager.load_from_file(data_manager.matches_file)

    # Creamos instancias para la clase Team
    teams = {team["id"]: Team(team["id"], team["code"], team["name"], team["group"])for team in teams_data}

    # Creamos instancias para la clase Stadium
    stadiums = {stadium["id"]: Stadium(stadium["id"], stadium["name"], stadium["city"], stadium["capacity"])for stadium in stadiums_data}

    # Agregamos los asientos para los estadios acorde al tipo de entrada:
    for stadium in stadiums.values():
        general_capacity, vip_capacity = stadium.capacity[0], stadium.capacity[1]
        stadium.set_seats(general_capacity, vip_capacity)

    # Creamos instancias para la clase Match
    matches = []
    for match in matches_data:
        try:
            # Definimos las variables para la busqueda de los partidos
            match_id = match["id"]
            match_number = match["number"]
            home_team_id = match["home"]["id"]
            away_team_id = match["away"]["id"]
            match_date = datetime.fromisoformat(match["date"])
            match_group = match["group"]
            stadium_id = match["stadium_id"]

            # Buscamos los equipos y estadios con los keys de "id"
            home_team = teams.get(home_team_id)
            away_team = teams.get(away_team_id)
            stadium = stadiums.get(stadium_id)

            # Manejamos los casos en los que no se encuentren los equipos o estadios
            if not home_team:
                print(f"Equipo local con ID {home_team_id} no encontrado para el partido {match_id}")
            if not away_team:
                print(f"Equipo visitante con ID {away_team_id} no encontrado para el partido {match_id}")
            if not stadium:
                print(f"Estadio con ID {stadium_id} no encontrado para el partido {match_id}")

            # Si se encuentran los equipos y estadios, creamos las instancias de Match
            if home_team and away_team and stadium:
                matches.append(
                    Match(
                        match_id,
                        match_number,
                        home_team,
                        away_team,
                        match_date,
                        match_group,
                        stadium,
                    )
                )
            else:
                print(f"Datos faltantes para el partido con id {match_id}")
        # Manejamos las posibles excepciones de tipo KeyError
        except KeyError as e:
            print(f"KeyError: {e} en el partido {match}")

    # Instanciamos la clase Sales
    sales = Sales()
    sales.load_data(clients_data, tickets_data)

    # Instanciamos la clase Assistance
    assistance = Assistance()
    assistance.load_data(tickets_data)

    # Instanciamos la clase Restaurant
    restaurant = Restaurant()
    restaurant.load_products(stadiums_data)

    # Instanciamos la clase RestaurantSales
    restaurant_sales = RestaurantSales(restaurant=restaurant, sales=sales)
    
    # Instanciamos la clase Statistics
    statistics = Statistics(sells_data=sells_data, sales=sales, matches=matches, assistance=assistance)

    # Ejecucion del programa:
    while True:
        # Imprimimos el menu
        print("\nSelecciona un modulo del menu: ")
        print("Opcion 1: Gestion de partidos y estadios ")
        print("Opcion 2: Gestion de ventas de entradas")
        print("Opcion 3: Gestion de asistencia a partidos ")
        print("Opcion 4: Gestion de restaurantes ")
        print("Opcion 5: Gestion de venta de restaurantes ")
        print("Opcion 6: Indicadores de gestion")
        print("Opcion 7: Salir \n")

        # Solicitamos al usuario que ingrese la opcion deseada
        option = int(input("Ingrese el numero de la opcion deseada: "))

        # Manejamos las opciones, acorde a los modulos existentes
        # Opcion 1: Filtrar partidos
        if option == 1:
            sec_option = int(input("\nSeleccione una opción: \n1. Filtrar partidos por equipo \n2. Filtrar partidos por estadio \n3. Filtrar partidos por fecha\n"))

            if sec_option == 1:
                for t in teams.values():
                    print(t.get_info())
                chosen_team = input("Ingrese el nombre del equipo: ")
                matching_teams = [team for team in teams.values() if team.name.lower() == chosen_team.lower()]
                
                if matching_teams:
                    chosen_team_obj = matching_teams[0]
                    print(f"\nFiltrando partidos por equipo {chosen_team_obj.name}:")
                    filtered_by_team = Match.filter_matches(matches, team=chosen_team_obj)
                    for match in filtered_by_team:
                        print(match.get_info())
                else:
                    print(f"No se encontró el equipo con nombre '{chosen_team}'.")

            elif sec_option == 2:
                print("\nEstadios disponibles: \n")
                for s in stadiums.values():
                    print(f'{s.get_info()}\n')
                chosen_stadium = input("Ingrese el nombre del estadio: ")
                matching_stadiums = [stadium for stadium in stadiums.values() if stadium.name.lower() == chosen_stadium.lower()]
                
                if matching_stadiums:
                    chosen_stadium_obj = matching_stadiums[0]
                    print(f"\nFiltrando partidos por estadio {chosen_stadium_obj.name}:")
                    filtered_by_stadium = Match.filter_matches(matches, stadium_id=chosen_stadium_obj.id)
                    for match in filtered_by_stadium:
                        print(match.get_info())
                else:
                    print(f"No se encontró el estadio con nombre '{chosen_stadium}'.")

            elif sec_option == 3:
                chosen_date = input("Ingrese la fecha del partido (YYYY-MM-DD): ")
                try:
                    chosen_date_obj = datetime.fromisoformat(chosen_date)
                    print(f"\nFiltrando partidos por fecha {chosen_date}:")
                    filtered_by_date = Match.filter_matches(matches, date=chosen_date_obj)
                    for match in filtered_by_date:
                        print(match.get_info())
                except ValueError:
                    print(f"Fecha inválida: {chosen_date}. Por favor ingrese la fecha en formato YYYY-MM-DD.")
        
        # Opcion 2: Gestión de ventas de entradas
        elif option == 2:
            sales.process_ticket_sale(matches)
            data_manager.save_data_to_file(
                [vars(client) for client in sales.clients.values()], data_manager.clients_file
            )
            data_manager.save_data_to_file(
                [ticket.to_dict() for ticket in sales.tickets], data_manager.tickets_file
            )

        # Opcion 3: Gestion de asistencia a partidos
        elif option == 3:
            ticket_id = input("Ingrese el ID del ticket para validar la autenticidad: ")
            valid, message = assistance.validate_authenticity(ticket_id)
            print(message)
            if valid:
                assistance.save_data(data_manager.tickets_file)
                print(message)

        # Opcion 4: Gestion de restaurantes
        elif option == 4:
            print("Gestión de Restaurantes: ")
            print("1. Buscar productos por nombre")
            print("2. Buscar productos por tipo")
            print("3. Buscar productos por rango de precio")
            sub_option = int(input("Ingrese la opción deseada: "))

            if sub_option == 1:
                name = input("Ingrese el nombre del producto: ")
                results = restaurant.search_by_name(name)
                if results:
                    for product in results:
                        print(f"\n{product.to_dict()} \n")
                else:
                    print("No se encontraron productos con ese nombre.\n")

            elif sub_option == 2:
                product_type = input("Ingrese el tipo de producto (food/drink): ")
                if product_type not in ["food", "drink"]:
                    print("Tipo de producto no válido.")
                else:
                    results = restaurant.search_by_type(product_type)
                    for product in results:
                        print(f"\n{product.to_dict()} \n")
            elif sub_option == 3:
                try:
                    min_price = float(input("Ingrese el precio mínimo: "))
                    max_price = float(input("Ingrese el precio máximo: "))
                    results = restaurant.search_by_price_range(min_price, max_price)
                    if results:
                        for product in results:
                            print(f"\n{product.to_dict()} \n")
                    else:
                        print(
                            "\nNo se encontraron productos en ese rango de precios.\n"
                        )
                except ValueError:
                    print("Ingrese valores numéricos válidos para el rango de precios.")
            else:
                print("Opción no válida en Gestión de Restaurantes.")
                
        # Opcion 5: Gestion de venta de restaurantes
        elif option == 5:
            print("Gestión de ventas en el restaurante")
            client_id = int(input("Ingrese la cédula del cliente: "))
            product_type = input(
                "Ingrese el tipo de producto que desea comprar (food/drink): "
            )
            print("Productos disponibles en el restaurante: ")
            for product in restaurant.products:
                if product.product_type == product_type:
                    print(f"{product.name} - ${product.price:.2f}")
            product_name = input("Ingrese el nombre del producto que desea comprar: ")
            product_quantity = int(
                input("Ingrese la cantidad de productos que desea comprar: ")
            )
            message, sale_data = restaurant_sales.sell_products(client_id, product_name, product_quantity, product_type)
            print(message)
            # Validamos que solo cuando la compra sea exitosa se actualice el inventario
            if "Compra exitosa" in message:
                updated_product = next((p for p in restaurant.products if p.name == product_name and p.product_type == product_type), None)
                # Si la compra es exitosa, actualizamos el inventario en el archivo txt
                if updated_product:
                    category = updated_product.category
                    try:
                        for stadium in stadiums_data:
                            for r in stadium.get('restaurants', []):
                                for product in r.get('products', []):
                                    if product['name'] == product_name and product['adicional'] == category:
                                        product['stock'] -= product_quantity
                        # Guardamos los cambios en el archivo txt
                        data_manager.save_data_to_file(stadiums_data, data_manager.stadiums_file)
                        # Recargamos los datos para poder trabajar basados en la nueva informacion
                        restaurant.load_products(stadiums_data)
                        sells_data.append(sale_data)
                        data_manager.save_data_to_file(sells_data, data_manager.sells_file)
                        
                    except Exception as e:
                        print(f"Error al actualizar el archivo stadiums.txt: {e}")
        # Mostramos las estadisticas y llamamos al metodo para generar los graficos en formato .png
        elif option == 6:
            statistics.show_statistics()

        # Opcion 7: Salir del programa
        elif option == 7:
            break
        
        else:
            print("\nOpción no válida. Por favor, intente de nuevo.")

    print("\nGracias por usar el programa de la EURO 2024, ¡vuelva pronto!")

if __name__ == '__main__':
    Main()
