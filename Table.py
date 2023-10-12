# basically a list of attributes and functional dependencies
import Attribute as A
import FunctionalDependency as FD

class Table:
    attributes: list[A.Attribute]
    functionalDependencies: list[FD.FunctionalDependency]
    
    def __init__(self, attributes: list[A.Attribute], functionalDependencies: list[FD.FunctionalDependency]) -> None:
        self.attributes = attributes
        self.functionalDependencies = functionalDependencies
         
    def isNF1(self) -> bool:
        return False
    
    def isNF2(self) -> bool:
        return False   
            

def normalizeTo1NF(table: Table) -> list[Table]:
    return None

def normalizeTo2NF(table: Table) -> list[Table]:
    pass

def normalizeTo3NF(table: Table) -> list[Table]:
    return None

def normalizeToBCNF(self, table: Table) -> list[Table]:
    return None
