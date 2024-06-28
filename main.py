# Importamos las librerias a utilizar
from matches_and_stadium_management.api import API
from matches_and_stadium_management.match import Match
from matches_and_stadium_management.team import Team
from matches_and_stadium_management.stadium import Stadium
from tickets_and_sales_management.sales import Sales
from assistance_management.assistance import Assistance
from restaurant_management.restaurant import Restaurant
from restaurant_management.restaurant_sales import RestaurantSales
from datetime import datetime
import os
from dotenv import load_dotenv
import json

# Cargamos el archivo dotenv
load_dotenv()

# Cargamos los endpoints de las apis desde el archivo dotenv
teams_api = os.getenv("TEAMS_API")
stadiums_api = os.getenv("STADIUMS_API")
matches_api = os.getenv("MATCHES_API")

# Creamos variables con la ruta de los archivos txt que generaremos
data_dir = "data"
teams_file = os.path.join(data_dir, "teams.txt")
stadiums_file = os.path.join(data_dir, "stadiums.txt")
matches_file = os.path.join(data_dir, "matches.txt")
clients_file = os.path.join(data_dir, "clients.txt")
tickets_file = os.path.join(data_dir, "tickets.txt")


# Creamos una funcion para que si no hay carpetas con la data, cree la carpeta y los archivos
def create_data_folder_and_files():
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    # Recorremos las rutas para crear los archivos en caso de que no existan
    for file_path in [
        teams_file,
        stadiums_file,
        matches_file,
        clients_file,
        tickets_file,
    ]:
        if not os.path.exists(file_path):
            # Intentamos crear los archivos
            try:
                with open(file_path, "w") as file:
                    file.write("[]")
            # Si falla, capturamos la excepcion y mostramos un mensaje
            except Exception as e:
                print(f"Error al crear el archivo {file_path}: {e}")


# Creamos una funcion para guardar datos dentro de un archivo
def save_data_to_file(data, file_name):
    with open(file_name, "w") as file:
        json.dump(data, file)


# Creamos una funcion para cargar los datos desde el archivo txt
def load_from_file(filename):
    if os.path.exists(filename):
        try:
            with open(filename, "r") as file:
                return json.load(file)
        except json.JSONDecodeError:
            print(
                f"Error al decodificar el archivo {filename}. El archivo puede estar vacío o malformado."
            )
    return None


# Pre cargamos la data y la guardamos en un archivo txt para poder manejarla sin llamar a la api de nuevo
def pre_load_data():
    teams_data = API.get_teams(teams_api)
    if teams_data:
        save_data_to_file(teams_data, teams_file)

    stadiums_data = API.get_stadiums(stadiums_api)
    if stadiums_data:
        save_data_to_file(stadiums_data, stadiums_file)

    matches_data = API.get_matches(matches_api)
    if matches_data:
        save_data_to_file(matches_data, matches_file)


# Funcion principal del programa
def Main():
    # Llamamos a la funcion para crear la carpeta data
    create_data_folder_and_files()

    # Cargamos los datos desde el archivo txt
    teams_data = load_from_file(teams_file)
    stadiums_data = load_from_file(stadiums_file)
    matches_data = load_from_file(matches_file)
    clients_data = load_from_file(clients_file)
    tickets_data = load_from_file(tickets_file)

    # Si no hay datos, los cargamos desde la API y los guardamos en un archivo txt
    if not teams_data or not stadiums_data or not matches_data:
        pre_load_data()
        # Cargamos nuevamente los datos
        teams_data = load_from_file(teams_file)
        stadiums_data = load_from_file(stadiums_file)
        matches_data = load_from_file(matches_file)

    # Creamos instancias para la clase Team
    teams = {
        team["id"]: Team(team["id"], team["code"], team["name"], team["group"])
        for team in teams_data
    }

    # Creamos instancias para la clase Stadium
    stadiums = {
        stadium["id"]: Stadium(
            stadium["id"], stadium["name"], stadium["city"], stadium["capacity"]
        )
        for stadium in stadiums_data
    }

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
                print(
                    f"Equipo local con ID {home_team_id} no encontrado para el partido {match_id}"
                )
            if not away_team:
                print(
                    f"Equipo visitante con ID {away_team_id} no encontrado para el partido {match_id}"
                )
            if not stadium:
                print(
                    f"Estadio con ID {stadium_id} no encontrado para el partido {match_id}"
                )

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
        
        # Opcion 2: Gestión de ventas de entradas
        if option == 2:
            sales.process_ticket_sale(matches)
            save_data_to_file(
                [vars(client) for client in sales.clients.values()], clients_file
            )
            save_data_to_file(
                [ticket.to_dict() for ticket in sales.tickets], tickets_file
            )

        # Opcion 3: Gestion de asistencia a partidos
        elif option == 3:
            ticket_id = input("Ingrese el ID del ticket para validar la autenticidad: ")
            valid, message = assistance.validate_authenticity(ticket_id)
            print(message)
            if valid:
                assistance.save_data(tickets_file)
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
            message = restaurant_sales.sell_products(
                client_id, product_name, product_quantity, product_type
            )
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
                        save_data_to_file(stadiums_data, stadiums_file)
                        # Recargamos los datos para poder trabajar basados en la nueva informacion
                        restaurant.load_products(stadiums_data)
                    except Exception as e:
                        print(f"Error al actualizar el archivo stadiums.txt: {e}")

        elif option == 6:
            # Código para indicadores de gestión
            pass

        if option == 7:
            break

    print("Gracias por usar el programa de la EURO 2024, ¡vuelva pronto!")

    # Modulo 1. Filtrar partidos:
    # print("\nFiltrar partidos por equipo 'Germany':")
    # filtered_by_team = Match.filter_matches(matches, team=teams['31c88261-1efd-444e-95ac-b7c1cd034bfd'])
    # for match in filtered_by_team:
    #     print(match.get_info())

    # print("\nFiltrar partidos por estadio 'Estadio Olímpico de Berlín': ")
    # filtered_by_stadium = Match.filter_matches(matches, stadium_id="2eead114-7627-45c4-83ab-ee3d66a6c62f")
    # for match in filtered_by_stadium:
    #     print(match.get_info())

    # print("\nFiltrar partidos por fecha '2024-06-14':")
    # filtered_by_date = Match.filter_matches(matches, date=datetime(2024, 6, 15))
    # for match in filtered_by_date:
    #     print(match.get_info())


Main()
