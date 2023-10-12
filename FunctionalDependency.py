# two lists of attributes
# one for the prime attributes and one for the non-prime attributes
import Attribute


class FunctionalDependency:
    determinants: set[Attribute.Attribute]
    nonDeterminants: set[Attribute.Attribute]
    
    def __init__(self, determinant: set[Attribute.Attribute], nonDeterminants: set[Attribute.Attribute]) -> None:
        #Attributes: sets of attributes determinants (left hand side) & nonDeterminants (right hand side) of a fucntional Dependency 
        #Returns:    nothing
        self.determinants = determinant
        self.nonDeterminants = nonDeterminants

    def __str__(self) -> str:
        returnString = "{ "
        for i, determinant in enumerate(self.determinants):
            returnString += determinant.__str__()
            if i < len(self.determinants) - 1:
                returnString += ", "
        returnString += "} -> { "
        for i, nonDeterminant in enumerate(self.nonDeterminants):
            returnString += nonDeterminant.__str__()
            if i < len(self.nonDeterminants) - 1:
                returnString += ", "
        returnString += "}"
        return returnString

