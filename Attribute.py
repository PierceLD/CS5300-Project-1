# basically a just a string (but probably more than that)

class Attribute:
    name: str
    isPrime: bool

    def __init__(self, name: str, isPrime: bool) -> None:
        self.name = name
        self.isPrime = isPrime
        
    def __str__(self) -> str:
        return self.name
    
    def set_isPrime(self, prime: bool) -> None:
        self.isPrime = prime
        