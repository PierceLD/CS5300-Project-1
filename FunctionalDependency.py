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

    """ Helper functions to return determinants as a set of strings in order
        to make set() operations work correctly (i.e. issuperset(), issubset(), etc)
        Input: self
        Output: set of determinant/non-determinant names
    """
    def getDeterminantNames(self) -> set[str]:
        return set([attr.name for attr in self.determinants])
    
    def getNonDeterminantNames(self) -> set[str]:
        return set([attr.name for attr in self.nonDeterminants])