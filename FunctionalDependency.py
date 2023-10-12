# two lists of attributes
# one for the prime attributes and one for the non-prime attributes
import Attribute


class FunctionalDependency:
    determinants: list[Attribute.Attribute]
    nonDeterminants: list[Attribute.Attribute]
    
    def __init__(self, determinant: list[Attribute.Attribute], nonDeterminants: list[Attribute.Attribute]) -> None:
        #Attributes: determinant (left hand side)  nonDeterminants (right hand side) of a fucntional Dependency 
        #Returns:    nothing
        determinants: set(Attribute.Attribute)
        nonDeterminants: set(Attribute.Attribute)

    def __init__(self, determinant: set(Attribute.Attribute), nonDeterminants: set(Attribute.Attribute),) -> None:
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

