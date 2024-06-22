from typing import List
from datetime import datetime as date
from .team import Team
from .stadium import Stadium
from .match import Match

# Creamos la clase match
class Match:
    def __init__(self, home_team: List[Team] , away_team: List[Team], date_time: date, stadium: List[Stadium]):
        self.home_team = home_team 
        self.away_team = away_team 
        self.date_time = date_time 
        self.stadium = stadium 
    
    # definimos el metodo para obtener informacion del partido 
    def get_info(self):
        return (f"The match is: {self.home_team.get_info()} vs {self.away_team.getinfo()} at {self.stadium.get_info()} on {self.date_time}")
    
    # Definimos el metodo para filtrar los partidos dependiendo de la fecha, equipo y estadio
    @staticmethod 
    def filter_matches(matches: List[Match], **props):
        # Creamos una lista para almacenar los partidos filtrados
        filtered_matches = []
        
        # Iteramos sobre los partidos para filtrarlos
        for match in matches: 
            match_date = props.get('date')
            match_team = props.get('team')
            match_stadium = props.get('stadium')
            
            # creamos condiciones para que se fitre dependiendo de el prop que reciba
            if match_date and match.date_time != match_date: 
                continue
            if match_team and match_team not in (match.home_team, match.away_team):
                continue
            if match_stadium and match_stadium != match.stadium:
                continue
            
            # Agregamos los partidos que cumplan con el filtro, en caso de que no hayan, se quedara la lista vacia
            filtered_matches.append(match)
        
        # Retornamos la lista de partidos filtrados
        return filtered_matches
    