from datetime import datetime as date
from typing import List

from matches_and_stadium_management.stadium import Stadium
from matches_and_stadium_management.team import Team


# Creamos la clase match
class Match:
    def __init__(
        self,
        id: int,
        number: int,
        home_team: List[Team],
        away_team: List[Team],
        date_time: date,
        group: str,
        stadium: List[Stadium],
    ):
        self.id = id
        self.number = number
        self.group = group
        self.home_team = home_team
        self.away_team = away_team
        self.date_time = date_time
        self.stadium = stadium

    # definimos el metodo para obtener informacion del partido
    def get_info(self):
        return f"The match is: {self.home_team.get_info()} vs {self.away_team.get_info()} at {self.stadium.get_info()} on {self.date_time}"

    # Definimos el metodo para transformar la informacion del partido de objeto a string
    def __str__(self):
        return self.get_info()

    # Definimos el metodo para retornar un string imprimible con la informacion del partido
    def __repr__(self):
        return self.__str__()

    # Definimos el metodo para filtrar los partidos dependiendo de la fecha, equipo y estadio
    @staticmethod
    def filter_matches(matches, **props):
        # Creamos una lista para almacenar los partidos filtrados
        filtered_matches = []

        # Iteramos sobre los partidos para filtrarlos
        for match in matches:
            match_date = props.get("date")
            match_team = props.get("team")
            match_stadium = props.get("stadium_id")

            # creamos condiciones para que se fitre dependiendo de el prop que reciba
            if match_date and match.date_time != match_date:
                continue
            if match_team and match_team not in (match.home_team, match.away_team):
                continue
            if match_stadium and (match_stadium != match.stadium.id):
                continue

            # Agregamos los partidos que cumplan con el filtro, en caso de que no hayan, se quedara la lista vacia
            filtered_matches.append(match)

        # Retornamos la lista de partidos filtrados
        return filtered_matches
