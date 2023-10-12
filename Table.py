# basically a list of attributes and functional dependencies
import Attribute as A
import FunctionalDependency as FD

class Table:
    attributes: list[A.Attribute]
    functionalDependencies: set[FD.FunctionalDependency]
    
    def __init__(self, attributes: list[A.Attribute], functionalDependencies: list[FD.FunctionalDependency]) -> None:
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
    newTables: set[Table] = {}
    for functionalDependency in table.functionalDependencies:
        for attribute in functionalDependency.determinants:
            if attribute.isPrime == False:
                #creates a new table with the non-prime attribute as the deterimant and other attributes of functional dependency and only one functional dependency
                newTable: Table = Table({attribute,functionalDependency.nonDeterminants}, functionalDependency)
                newTable.attributes[0].set_isPrime(True)
                newTables.add(newTable)
            # else:
            #     #else if attribute is prime 
            #     newTable: Table = Table({functionalDependency.determinants,functionalDependency.nonDeterminants}, functionalDependency)
            #     newTables.add(newTable)
                


          
def normalizeTo3NF(table: Table) -> set[Table]:
    return None

def normalizeToBCNF(self, table: Table) -> set[Table]:
    return None
