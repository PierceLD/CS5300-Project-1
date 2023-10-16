# basically a just a string (but probably more than that)

class Attribute:
    name: str
    isPrime: bool
    type: type
        
    def __init__(self, name: str, isPrime: bool = False) -> None:
        self.name = name
        self.isPrime = isPrime
        
    def __str__(self) -> str:
        return self.name
    
    