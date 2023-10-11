# basically a just a string (but probably more than that)

class Attribute:
    name: str
    
    def __init__(self, name: str) -> None:
        self.name = name
        
    def __str__(self) -> str:
        return self.name
        