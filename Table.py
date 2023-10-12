# basically a list of attributes and functional dependencies
import Attribute as A
import FunctionalDependency as FD

class Table:
    attributes: list[A.Attribute]
    functionalDependencies: list[FD.FunctionalDependency]
    
    def __init__(self, attributes: list[A.Attribute], functionalDependencies: list[FD.FunctionalDependency]) -> None:
        self.attributes = attributes
        self.functionalDependencies = functionalDependencies
         
    def is1NF(self) -> bool:
        return False
    
    def is2NF(self) -> bool:
        #Attributes: none
        #True if table is in 2NF
        #Returns: boolean
        primeAttributes: set[A.Attribute] = set(self.getPrimeAttributes())
        for functionalDependency in self.functionalDependencies:
             if functionalDependency.determinants != primeAttributes:
                 return False
             
                 
                 
    def getPrimeAttributes(self) -> list[A.Attribute]:
        #Attributes: none
        #gets all the prime attributes in the relation
        #Returns: list of Attribute
        return [attr for attr in self.attributes if attr.isPrime]
                


def normalizeTo1NF(table: Table) -> set[Table]:
    return None

def normalizeTo2NF(table: Table) -> set[Table]:
    newTables: set[Table] = {}
    addDepedency: bool = True
    for functionalDependency in table.functionalDependencies:
        if functionalDependency.determinants !=
                


          
def normalizeTo3NF(table: Table) -> set[Table]:
    return None

def normalizeToBCNF(self, table: Table) -> set[Table]:
    return None
