# basically a list of attributes and functional dependencies
import Attribute as A
import FunctionalDependency as FD

class Table:
    attributes: set[A.Attribute]
    functionalDependencies: set[FD.FunctionalDependency]
    
    def __init__(self, attributes: set[A.Attribute], functionalDependencies: set[FD.FunctionalDependency]) -> None:
        self.attributes = attributes
        self.functionalDependencies = functionalDependencies
        self.primeAttributes = self.getPrimeAttributes()
        
    def is1NF(self) -> bool:
        for attribute in self.attributes:
            if attribute.isMultiValued:
                return False
        return True
    
    def is2NF(self) -> bool:
        for functionalDependency in self.functionalDependencies:
             if functionalDependency.determinants != set(self.primeAttributes):
                 for attribute in functionalDependency.determinants:
                     if attribute.isPrime:
                         return False
        return True
                     
    def is3NF(self) -> bool:
        if not self.is2NF():
            return False
        for functionalDependency in self.functionalDependencies:
            for attr in functionalDependency.nonDeterminants:
                if attr.isPrime == True:
                    return True
        for functionalDependency in self.functionalDependencies:
            if not self.isSuperkey(functionalDependency.determinants):
                return False
        return True

    def isBCNF(self):
        for functionalDependency in self.functionalDependencies:
            if not self.isSuperkey(functionalDependency.determinants):
                return False
        return True
    
    def isBCNF(self) -> bool:
        return False
    
    def isSuperkey(self, attributes: list[A.Attribute]) -> bool:
        # Helper function to check if a set of attributes is a superkey
        return set(attributes).issuperset(self.primeAttributes)
 
    def getPrimeAttributes(self) -> list[A.Attribute]:
        #gets all the prime attributes in the relation
        return [attr for attr in self.attributes if attr.isPrime]
                     
    def __str__(self) -> str:
        i = len(self.attributes)
        if i == 0:
            return "No attributes available."

        max_name_length = max(len(attr.name) for attr in self.attributes)
        total_width = (max_name_length + 4) * len(self.attributes) + 10
        border = "+" + "-" * (total_width - 2) + "+\n"
        result = border

        names = " | ".join([f"{'(PK)' if attr.isPrime else ''}{attr.name:{max_name_length}}" for attr in self.attributes])
        result += f"| {names:{total_width - 4}} |\n"  # Adjusted alignment and spacing
        result += border


        result += "Functional Dependencies:\n"
        for fd in self.functionalDependencies:
            result+="\t" + fd.__str__() + "\n"
        return result
                 
    def getPrimeAttributes(self) -> set[A.Attribute]:
        #Attributes: none
        #gets all the prime attributes in the relation
        #Returns: set of Attribute
        return [attr for attr in self.attributes if attr.isPrime]
                


def normalizeTo1NF(table: Table) -> set[Table]:
    if table.is1NF():
        return table
       
    newTables: set[Table] = set()
    for attribute in table.attributes:
        if attribute.dataType == "LIST":
            newDependent: set[A.Attribute] = {attribute}
            newFunctionalDependency: FD.FunctionalDependency = FD.FunctionalDependency(table.getPrimeAttributes(), newDependent)
            newTable: Table = Table(table.getPrimeAttributes().union(newDependent), newFunctionalDependency)
            newTables.add(newTable)
    return newTables

def normalizeTo2NF(table: Table) -> set[Table]:
    if table.is2NF():
        return table
    
    table = normalizeTo1NF(table)
    
    normalized: set[Table] = set()
    for functionalDependency in table.functionalDependencies:
        #Add new table with functional dependency attributes and with the functional dependency itself
        normalized.add(Table(set(functionalDependency.determinants) + set(functionalDependency.nonDeterminants),[functionalDependency]))
    return normalized
        

def normalizeTo3NF(table: Table) -> set[Table]:
    if table.is3NF():
        return table
    
    table = normalizeTo2NF(table)
    
    normalized: set[Table] = set()
    for functionalDependency in table.functionalDependencies:
        for attr in functionalDependency.determinants:
            attr.set_isPrime(True)
        #Add new table with functional dependency attributes and with the functional dependency itself
        normalized.add(Table(list(functionalDependency.determinants) + list(functionalDependency.nonDeterminants),[functionalDependency]))
    return normalized

def normalizeToBCNF(table: Table) -> set[Table]:
    noramlized: set[Table] = set()
    for functionalDependency in table.functionalDependencies:
        if not table.isSuperkey(functionalDependency.determinants):
            #R-A and XA in the form X->A in Relation R 
            newAttrs = list(set(table.attributes).difference(functionalDependency.nonDeterminants))
            for attr in functionalDependency.determinants:
                attr.set_isPrime(True)
            relation1 = Table()

