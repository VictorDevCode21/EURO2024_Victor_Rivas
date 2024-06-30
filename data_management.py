import os
import json
from matches_and_stadium_management.api import API
from dotenv import load_dotenv

# Clase para manejar la carga de los datos desde las api y crear las carpetas y archivos en las rutas especificadas.
class DataManager:
    def __init__(self):
        load_dotenv()
        self.data_dir = "data"
        self.teams_file = os.path.join(self.data_dir, "teams.txt")
        self.stadiums_file = os.path.join(self.data_dir, "stadiums.txt")
        self.matches_file = os.path.join(self.data_dir, "matches.txt")
        self.clients_file = os.path.join(self.data_dir, "clients.txt")
        self.tickets_file = os.path.join(self.data_dir, "tickets.txt")
        self.sells_file = os.path.join(self.data_dir, "sells.txt")
        self.teams_api = os.getenv("TEAMS_API")
        self.stadiums_api = os.getenv("STADIUMS_API")
        self.matches_api = os.getenv("MATCHES_API")
        
        self.create_data_folder_and_files()

    def create_data_folder_and_files(self):
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

        for file_path in [
            self.teams_file,
            self.stadiums_file,
            self.matches_file,
            self.clients_file,
            self.tickets_file,
            self.sells_file
        ]:
            if not os.path.exists(file_path):
                try:
                    with open(file_path, "w") as file:
                        file.write("[]")
                except Exception as e:
                    print(f"Error al crear el archivo {file_path}: {e}")

    def save_data_to_file(self, data, file_name):
        with open(file_name, "w") as file:
            json.dump(data, file)

    def load_from_file(self, filename):
        if os.path.exists(filename):
            try:
                with open(filename, "r") as file:
                    return json.load(file)
            except json.JSONDecodeError:
                print(
                    f"Error al decodificar el archivo {filename}. El archivo puede estar vacío o malformado."
                )
        return None

    def pre_load_data(self):
        teams_data = API.get_teams(self.teams_api)
        if teams_data:
            self.save_data_to_file(teams_data, self.teams_file)

        stadiums_data = API.get_stadiums(self.stadiums_api)
        if stadiums_data:
            self.save_data_to_file(stadiums_data, self.stadiums_file)

        matches_data = API.get_matches(self.matches_api)
        if matches_data:
            self.save_data_to_file(matches_data, self.matches_file)