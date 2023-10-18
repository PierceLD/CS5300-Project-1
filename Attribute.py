# basically a just a string (but probably more than that)

class Attribute:
    name: str
    isPrime: bool
    isMultiValued: bool
    dataType: str # SQL data type: "VARCHAR" for a str, "INT" for int, "DATE" for date, "FLOAT" for float

    def __init__(self, name: str, isPrime: bool = False, isMultiValued: bool = False, dataType: str = "VARCHAR") -> None:
        self.name = name
        self.isPrime = isPrime
        self.isMultiValued = isMultiValued
        self.dataType = dataType
        
    def __str__(self) -> str:
        return self.name
    
    