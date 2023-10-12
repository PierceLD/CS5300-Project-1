# two lists of attributes
# one for the prime attributes and one for the non-prime attributes
import Attribute

class FunctionalDependency:
    determinants: list[Attribute.Attribute]
    nonDeterminants: list[Attribute.Attribute]
    
    def __init__(self, determinant: list[Attribute.Attribute], nonDeterminants: list[Attribute.Attribute]) -> None:
        self.determinants = determinant
        self.nonDeterminants = nonDeterminants
        
    def __str__(self) -> str:
        returnString: str = "{ "
        for determinant in self.determinants:
            returnString += determinant.__str__() + ", "
        returnString += "} -> { "
        for nonDeterminant in self.nonPrimeAttributes:
            returnString += nonDeterminant.__str__() + ", "
        returnString += "}"
        return returnString

