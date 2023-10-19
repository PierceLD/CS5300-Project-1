# two lists of attributes
# one for the prime attributes and one for the non-prime attributes
import Attribute


class FunctionalDependency:
    determinants: set[Attribute.Attribute]
    nonDeterminants: set[Attribute.Attribute]
    isMultiValued: bool
    
    def __init__(self, determinants: set[Attribute.Attribute], nonDeterminants: set[Attribute.Attribute], isMultiValued: bool = False) -> None:
        #Attributes: sets of attributes determinants (left hand side) & nonDeterminants (right hand side) of a functional Dependency 
        #Returns:    nothing
        self.determinants = determinants
        self.nonDeterminants = nonDeterminants
        self.isMultiValued = isMultiValued

    def __str__(self) -> str:
        returnString = "{"
        for i, determinant in enumerate(self.determinants):
            returnString += determinant.__str__()
            if i < len(self.determinants) - 1:
                returnString += ", "
        returnString += "} -> {"
        for i, nonDeterminant in enumerate(self.nonDeterminants):
            returnString += nonDeterminant.__str__()
            if i < len(self.nonDeterminants) - 1:
                returnString += ", "
        returnString += "}"
        return returnString

