class Player:
    def __init__(self, player_id: int = None, code_name: str = None, equipment_id: int = None, team: str = None):
        self.player_id = player_id
        self.code_name = code_name
        self.equipment_id = equipment_id
        self.team = team  # 'Red' or 'Green'
        self.score = 0
        self.base_hit = False  # Tracks if player hit a base
    
    def __str__(self):
        return f"Player(ID: {self.player_id}, Name: {self.code_name}, Team: {self.team}, Score: {self.score})"
