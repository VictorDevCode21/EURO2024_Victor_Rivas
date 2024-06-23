# Importamos las librerias a utilizar
from matches_and_stadium_management.api import API
from matches_and_stadium_management.match import Match
from matches_and_stadium_management.team import Team
from matches_and_stadium_management.stadium import Stadium
import os
import requests as req
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
            with open(file_path, 'w') as file:
                file.write("[]")

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
    
    
    
    
    

if __name__ == '__main__':
    Main()