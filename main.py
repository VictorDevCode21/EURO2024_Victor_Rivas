# Importamos las librerias a utilizar
from matches_and_stadium_management.api import API
from matches_and_stadium_management.match import Match
from matches_and_stadium_management.team import Team
from matches_and_stadium_management.stadium import Stadium
from datetime import datetime
import os
from dotenv import load_dotenv
import json 

# Cargamos el archivo dotenv
load_dotenv() 

# Cargamos los endpoints de las apis desde el archivo dotenv
teams_api = os.getenv('TEAMS_API')
stadiums_api = os.getenv('STADIUMS_API')
matches_api = os.getenv('MATCHES_API')

# Creamos variables con la ruta de los archivos txt que generaremos
data_dir = "data"
teams_file =  os.path.join(data_dir, "teams.txt")
stadiums_file = os.path.join(data_dir, "stadiums.txt")
matches_file = os.path.join(data_dir, "matches.txt")




# Creamos una funcion para que si no hay carpetas con la data, cree la carpeta y los archivos
def create_data_folder_and_files():
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    
    # 
    for file_path in [teams_file, stadiums_file, matches_file]:
        if not os.path.exists(file_path):
            # Intentamos crear los archivos 
            try:
                with open(file_path, 'w') as file:
                    file.write("[]")
            # Si falla, capturamos la excepcion y mostramos un mensaje
            except Exception as e:
                print(f"Error al crear el archivo {file_path}: {e}")

# Creamos una funcion para guardar datos dentro de un archivo
def save_data_to_file(data, file_name):
    with open(file_name, 'w') as file:
        json.dump(data, file)
        
# Creamos una funcion para cargar los datos desde el archivo txt
def load_from_file(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            return json.load(file)
    return None

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
        

def Main():
    # Llamamos a la funcion para crear la carpeta data
    create_data_folder_and_files()
    
    # Cargamos los datos desde el archivo txt
    teams_data = load_from_file(teams_file)
    stadiums_data = load_from_file(stadiums_file)
    matches_data = load_from_file(matches_file)
    
    # Si no hay datos, los cargamos desde la API y los guardamos en un archivo txt
    if not teams_data or not stadiums_data or not matches_data:
        pre_load_data()
        # Cargamos nuevamente los datos
        teams_data = load_from_file(teams_file)
        stadiums_data = load_from_file(stadiums_file)
        matches_data = load_from_file(matches_file)
        
        
    # Creamos instancias para la clase Team 
    teams = {team['id']: Team(team['id'], team['code'], team['name'], team['group']) for team in teams_data}
    
    # Creamos instancias para la clase Stadium
    stadiums = {stadium['id']: Stadium(stadium['id'], stadium['name'], stadium['city'], stadium['capacity']) for stadium in stadiums_data}
    
    # Creamos instancias para la clase Match
    matches = []
    for match in matches_data:
        try:
            match_id = match['id']
            match_number = match['number']
            home_team_id = match['home']['id']
            away_team_id = match['away']['id']
            match_date = datetime.fromisoformat(match['date'])
            match_group = match['group']
            stadium_id = match['stadium_id']

            home_team = teams.get(home_team_id)
            away_team = teams.get(away_team_id)
            stadium = stadiums.get(stadium_id)
            
            if not home_team:
                print(f"Equipo local con ID {home_team_id} no encontrado para el partido {match_id}")
            if not away_team:
                print(f"Equipo visitante con ID {away_team_id} no encontrado para el partido {match_id}")
            if not stadium:
                print(f"Estadio con ID {stadium_id} no encontrado para el partido {match_id}")

            if home_team and away_team and stadium:
                matches.append(Match(match_id, match_number, home_team, away_team, match_date, match_group, stadium))
            else:
                print(f"Datos faltantes para el partido con id {match_id}")
        except KeyError as e:
            print(f"KeyError: {e} en el partido {match}")

    print(matches)
    
    # for match in matches:
    #     print(match.get_info())

Main()