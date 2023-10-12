# basically a list of attributes and functional dependencies
import Attribute as A
import FunctionalDependency as FD

class Table:
    attributes: set[A.Attribute]
    functionalDependencies: set[FD.FunctionalDependency]
    
    def __init__(self, attributes: set[A.Attribute], functionalDependencies: list[FD.FunctionalDependency]) -> None:
        self.attributes = attributes
        self.functionalDependencies = functionalDependencies
         
    def is1NF(self) -> bool:
        return False
    
    def is2NF(self) -> bool:
        for functionalDependency in self.functionalDependencies:
             for attribute in functionalDependency.determinants:
                 if attribute.isPrime == False:
                     return False  
            

def normalizeTo1NF(table: Table) -> set[Table]:
    return None

def normalizeTo2NF(table: Table) -> set[Table]:
    newTables: set[Table]
    for functionalDependency in table.functionalDependencies:
        for attribute in functionalDependency.determinants:
            if attribute.isPrime == False:
                pass


          
def normalizeTo3NF(table: Table) -> set[Table]:
    return None

def normalizeToBCNF(self, table: Table) -> set[Table]:
    return None
