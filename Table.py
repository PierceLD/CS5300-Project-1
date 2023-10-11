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
            

def normalizeToNF1(table: Table) -> list[Table]:
    return None

def normalizeToNF2(table: Table) -> list[Table]:
    return None

def normalizeToNF3(table: Table) -> list[Table]:
    return None

def normalizeToBCNF(table: Table) -> list[Table]:
    return None
