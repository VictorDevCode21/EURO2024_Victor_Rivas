import typing


class Team:
    def __init__(self, name: str, fifa_code: str, group: str):
        self.name = name 
        self.fifa_code = fifa_code 
        self.group = group 
        
    def get_info(self):
        return f"Team: {self.name}  Code: ({self.fifa_code}) - Group: {self.group}"
    