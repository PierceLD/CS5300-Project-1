# two lists of attributes
# one for the prime attributes and one for the non-prime attributes
import Attribute


class FunctionalDependency:
    determinants: set[Attribute.Attribute]
    nonDeterminants: set[Attribute.Attribute]
    
    def __init__(self, determinant: set[Attribute.Attribute], nonDeterminants: set[Attribute.Attribute]) -> None:
        #Attributes: determinant (left hand side)  nonDeterminants (right hand side) of a fucntional Dependency 
        #Returns:    nothing
        self.determinants = determinant
        self.nonDeterminants = nonDeterminants

    def __str__(self) -> str:
        returnString: str = "{ "
        for determinant in self.determinants:
            returnString += determinant.__str__() + ", "
        returnString += "} -> { "
        for nonDeterminant in self.nonDeterminants:
            returnString += nonDeterminant.__str__() + ", "
        returnString += "}"
        return returnString

