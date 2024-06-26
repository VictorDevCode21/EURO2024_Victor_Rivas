# Importamos las librerias a utilizar
import requests as req
from dotenv import load_dotenv
import os

# Cargamos el archivo dotenv
load_dotenv() 

# Cargamos los endpoints de las apis desde el archivo dotenv
teams_api = os.getenv('TEAMS_API')
stadiums_api = os.getenv('STADIUMS_API')
matches_api = os.getenv('MATCHES_API')

# Creamos una clase API para hacer las solicitudes a los endpoints
class API:
    @staticmethod
    # Definimos un metodo estatico para obtener los equipos
    def get_teams(teams_api):
        try:
            res = req.get(teams_api)
            # Levantamos una excepcion para los codigos de estado http
            res.raise_for_status()
            return res.json()
        except req.exceptions.RequestException as e:
            print(f"Error al hacer la petición a la API para obtener los equipos: {e}")
            return None

    @staticmethod
    # Definimos un metodo estatico para obtener los estadios
    def get_stadiums(stadiums_api):
        try:
            res = req.get(stadiums_api)
            # Levantamos una excepcion para los codigos de estado http
            res.raise_for_status()
            return res.json()
        except req.exceptions.RequestException as e:
            print(f"Error al hacer la petición a la API para obtener los estadios: {e}")
            return None

    @staticmethod
    # Definimos un metodo estatico para obtener los partidos
    def get_matches(matches_api):
        try:
            res = req.get(matches_api)
            # Levantamos una excepcion para los codigos de estado http
            res.raise_for_status()
            return res.json()
        # Capturamos la excepcion en caso de que falle la peticion y la mostramos
        except req.exceptions.RequestException as e:
            print(f"Error al hacer la petición a la API para obtener los partidos: {e}")
            return None



