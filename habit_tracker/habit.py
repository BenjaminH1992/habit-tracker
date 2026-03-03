from datetime import datetime

class Habit:

    def __init__(self, name: str, category: str, habit_id: int = None, created_at: str = None) -> None:
        self.id = habit_id
        self.name = name
        self.category = category
        self.created_at = created_at

    def __repr__(self):
        return f"<Habit(id={self.id}): , name='{self.name}', category='{self.category}', created_at='{self.created_at}>"
    
