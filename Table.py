# basically a list of attributes and functional dependencies
from copy import deepcopy
import Attribute as A
import FunctionalDependency as FD

class Table:
    name: str
    attributes: set[A.Attribute]
    primaryKey: set[A.Attribute]
    functionalDependencies: set[FD.FunctionalDependency]
    
    def __init__(self, attributes: set[A.Attribute], primaryKey: set[A.Attribute], functionalDependencies: set[FD.FunctionalDependency], name: str = "") -> None:
        self.attributes = attributes
        self.primaryKey = primaryKey
        self.functionalDependencies = functionalDependencies
        self.name = name
        
    # def TableDeepCopy(self, attributes: set[A.Attribute], primaryKey: set[A.Attribute], functionalDependencies: set[FD.FunctionalDependency], name: str = "") -> Table:
    
    def is1NF(self) -> bool:
        for attribute in self.attributes:
            if attribute.isMultiValued:
                return False
        return True
    
    def is2NF(self) -> bool:
        if not self.is1NF():
            return False
        for functionalDependency in self.functionalDependencies:
            if set(functionalDependency.determinants) != set(self.getPrimeAttributes()):
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
        if not self.is3NF():
            return False
        for functionalDependency in self.functionalDependencies:
            if not self.isSuperkey(functionalDependency.determinants):
                return False
        return True
    
    def is4NF(self) -> bool:
        if not self.isBCNF():
            return False
        for functionalDependency in self.functionalDependencies:
            if functionalDependency.isMultiValued:
                return False
        return True
    
    def is5NF(self) -> bool:
        if not self.is4NF():
            return False
        return False

    
    def isSuperkey(self, attributes: set[A.Attribute]) -> bool:
        # Helper function to check if a set of attributes is a superkey
        if len(self.getPrimeAttributes()) > 0:
            return attributes.issuperset(self.getPrimeAttributes()) 
        else:
            return False

    def getPrimeAttributes(self) -> set[A.Attribute]:
        #gets all the prime attributes in the relation
        return {attr for attr in self.attributes if attr.isPrime}
    
    def isTrivialMultiValuedDependency(self, functionalDependency: FD.FunctionalDependency) -> bool:
        return functionalDependency.isMultiValued and self.attributes is functionalDependency.determinants.union(functionalDependency.nonDeterminants)

    """ Helper function to return attributes as a set of strings in order
        to make set() operations work correctly (i.e. issuperset(), issubset(), etc)
        Input: self
        Output: set of attribute names
    """
    def getAttributeNames(self) -> set[str]:
        return set([attr.name for attr in self.attributes])

    def __str__(self) -> str:
        if len(self.attributes) == 0:
            return "No attributes available."
        elif len(self.getPrimeAttributes()) == 0:
            return "No prime attributes available"

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
                

def normalizeTo1NF(table: Table) -> set[Table]:
    if table.is1NF():
        return {table}

    newTables: set[Table] = set()
    multiValuedAttributes: set[A.Attribute] = set()
    for attribute in table.attributes:
        if attribute.isMultiValued:
            multiValuedAttributes.add(attribute)
            attribute.isPrime = True # make the attribute a key value
            newDependent: set[A.Attribute] = {attribute}
            newFunctionalDependency: FD.FunctionalDependency = FD.FunctionalDependency(table.primaryKey, newDependent)
            newPrimaryKey: set[A.Attribute] = table.primaryKey.union(attribute)
            newTable: Table = Table(table.getPrimeAttributes().union(newDependent), newPrimaryKey, {newFunctionalDependency}, table.name)
            newTables.add(newTable)

    newTable: Table = Table()
    return newTables

def normalizeTo2NF(table: Table) -> set[Table]:
    if table.is2NF():
        return {table}

    newTables: set[Table] = set()
    for functionalDependency in table.functionalDependencies:
        #Add new table with functional dependency attributes and with the functional dependency itself
        newAttrs: set[A.Attribute] = functionalDependency.determinants.union(functionalDependency.nonDeterminants)
        newTable: Table = Table(newAttrs, {functionalDependency})
        newTables.add(newTable)
    return newTables
        
def normalizeTo3NF(table: Table) -> set[Table]:
    if table.is3NF():
        return {table}
    #TODO: fix line below. normalizeToXNF returns a set when we only want to normalize one table at a time. add another for loop? idk
    #We should do this kind of stuff in Main
    # table = normalizeTo2NF(table)

    newTables: set[Table] = set()
    for functionalDependency in table.functionalDependencies:
        #Add new table with functional dependency attributes and with the functional dependency itself
        newAttrs = functionalDependency.determinants.union(functionalDependency.nonDeterminants)
        newTable = Table(newAttrs, {functionalDependency})
        newTables.add(deepcopy(newTable))

    for relation in newTables:
        for dependency in relation.functionalDependencies:
            for attr in dependency.determinants:
                attr.isPrime = True
            
        
    return newTables

def normalizeToBCNF(table: Table) -> set[Table]:
    if table.isBCNF():
        return {table}

    newTables: set[Table] = set()
    for functionalDependency in table.functionalDependencies:
        #find the functional dependency that is not in BCNF
        if not table.isSuperkey(functionalDependency.determinants):
            #R-A in the form of X->A in Relation R
            newAttrs = table.attributes.difference(functionalDependency.nonDeterminants)
            newFunctionalDependency = FD.FunctionalDependency(newAttrs, newAttrs)
            newTable = Table(newAttrs, {newFunctionalDependency})
            newTables.add(deepcopy(newTable))
            #XA in the form of X->A in Relation R
            newAttrs = functionalDependency.determinants.union(functionalDependency.nonDeterminants)
            newTable = Table(newAttrs, {functionalDependency})
            newTables.add(deepcopy(newTable))
    return newTables

def normalizeTo4NF(table: Table) -> set[Table]:
    if table.is4NF():
        return {table}
    newTables: set[Table] = set()
    removedAttributes: set[A.Attribute] = set()
    nonMultiValuedDependency: set[FD.FunctionalDependency] = set()
    for functionalDependency in table.functionalDependencies:
        if not table.isTrivialMultiValuedDependency(functionalDependency):
            #create new table that is trivial
            newAttributes: set[A.Attribute] = deepcopy(functionalDependency.determinants.union(functionalDependency.nonDeterminants))
            removedAttributes.add(functionalDependency.nonDeterminants)
            newTable: Table =  Table(newAttributes, newAttributes, functionalDependency)
            newTables.add(newTable)
        elif not functionalDependency.isMultiValued:
            nonMultiValuedDependency.add(functionalDependency)
            
    # make a new table that has all the removed attributes
    newAttributes: set[A.Attribute] = table.attributes.difference(removedAttributes)
    newPrimaryKey: set[A.Attribute] = deepcopy(table.primaryKey)
    newTables.add(Table(newAttributes, newPrimaryKey, nonMultiValuedDependency))
    return newTables
    
def normalizeTo5NF(table: Table) -> set[Table]:
    if table.is5NF():
        return {table}