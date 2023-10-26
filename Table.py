# basically a list of attributes and functional dependencies
from copy import deepcopy
import Attribute as A
import FunctionalDependency as FD

class Table:
    name: str
    attributes: set[A.Attribute]
    primaryKey: set[A.Attribute]
    functionalDependencies: set[FD.FunctionalDependency]
    
    def __init__(self, attributes: set[A.Attribute], functionalDependencies: set[FD.FunctionalDependency], name: str = "") -> None:
        self.attributes = attributes
        self.primaryKey = self.getPrimeAttributes()
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
            # if any of the determinants are a proper subset of the primary key (indicates partial FD)
            if functionalDependency.getDeterminantNames() < set([key.name for key in self.primaryKey]):
                return False
        return True

    def is3NF(self) -> bool:
        if not self.is2NF():
            return False

        # check for each FD if determinant is a superkey or if dependent is a prime attribute
        for functionalDependency in self.functionalDependencies:
            determinant_not_superkey: bool = not self.isSuperkey(functionalDependency.determinants)
            non_determinant_not_prime: bool = True
            for attr in functionalDependency.nonDeterminants: # find out if non-determinant is prime or not
                if attr.isPrime:
                    non_determinant_not_prime = False
            if determinant_not_superkey and non_determinant_not_prime: # if all attributes in FD are non-prime, indicates a transitive FD
                return False

        return True
    
    def isBCNF(self):
        if not self.is3NF():
            return False
        for functionalDependency in self.functionalDependencies:
            if not self.isSuperkey(functionalDependency.determinants): # if the FD determinant is not a superkey, violates BCNF constraint
                return False
        return True
    
    def is4NF(self) -> bool:
        if not self.isBCNF():
            return False
        for functionalDependency in self.functionalDependencies:
            if functionalDependency.isMultiValued and (len(functionalDependency.nonDeterminants) > 1):
                return False
        return True
    
    def is5NF(self) -> bool:
        if not self.is4NF():
            return False
        return False

    
    def isSuperkey(self, attributes: set[A.Attribute]) -> bool:
        # Helper function to check if a set of attributes is a superkey
        if len(self.getPrimeAttributes()) > 0:
            attributeNames: set[str] = set([attr.name for attr in attributes])
            return attributeNames.issuperset(set([key.name for key in self.getPrimeAttributes()])) 
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
                
""" The following are the normalization functions (1NF to 5NF)
    for each table.
    Input: A relation table
    Output: The decomposed relation table in specified normal form
"""
def normalizeTo1NF(table: Table) -> set[Table]:
    if table.is1NF():
        return {table}

    newTable: Table = deepcopy(table) # create a new copy of the table

    for attribute in newTable.attributes:
        if attribute.isMultiValued:
            attribute.isPrime = True # make the attribute a key value and not multi-valued
            attribute.isMultiValued = False
            if attribute.name[-1] == 's': # make it singular if it's plural
                attribute.name = attribute.name[:-1]
            newTable.primaryKey.add(attribute) # add the attribute to the table's primary key

    return {newTable}

def normalizeTo2NF(table: Table) -> set[Table]:
    if table.is2NF():
        return {table}
    
    newTables: set[Table] = set()
    originalTable: Table = deepcopy(table)
    # go thru FDs to find full FDs, where determinant = primary key, and partial FDs first
    for functionalDependency in originalTable.functionalDependencies:
        # if it's a full FD with determinant == primary key, just make a new table with all attributes from FD
        if functionalDependency.getDeterminantNames() == set([key.name for key in originalTable.primaryKey]):
            newAttrs: set[A.Attribute] = functionalDependency.determinants.union(functionalDependency.nonDeterminants)
            newTable: Table = Table(newAttrs, {functionalDependency}, originalTable.name) # new table's name is same as original table's
            newTables.add(deepcopy(newTable))
        # if it's a partial FD where determinant is proper subset of primary key
        elif functionalDependency.getDeterminantNames() < set([key.name for key in originalTable.primaryKey]):
            newAttrs: set[A.Attribute] = functionalDependency.determinants.union(functionalDependency.nonDeterminants)
            primeAttributes: list[str] = [attr.name for attr in newAttrs if attr.isPrime]
            newTableName: str = "".join(primeAttributes)
            if originalTable.name[:-1] in newTableName:
                newTableName = originalTable.name[:-1]
            newTable: Table = Table(newAttrs, {functionalDependency}, newTableName + 's')
            newTables.add(deepcopy(newTable))

    # loop through FDs again to find transitive FDs, where determinant is not a subset of primary key
    for functionalDependency in originalTable.functionalDependencies:
        s1: set[A.Attribute] = functionalDependency.getDeterminantNames()
        s2: set[A.Attribute] = set([key.name for key in originalTable.primaryKey])
        if s1.difference(s2) == s1: # if current FD determinant is not in primary key (indicating transitive FD)
            for t in newTables:
                newFDs: set[FD.FunctionalDependency] = set()
                for fd in t.functionalDependencies:
                    # if current FD determinant is in any of the newTable's FD non-determinants
                    if functionalDependency.getDeterminantNames().issubset(fd.getNonDeterminantNames()):
                        # add current FD to newTable FD list and add attributes newTable attribute list
                        t.attributes = t.attributes.union(functionalDependency.nonDeterminants)
                        newFDs.add(functionalDependency)
                t.functionalDependencies = t.functionalDependencies.union(newFDs)

    return newTables
        
def normalizeTo3NF(table: Table) -> set[Table]:
    if table.is3NF():
        return {table}

    newTables: set[Table] = set()
    originalTable: Table = deepcopy(table)
    for functionalDependency in originalTable.functionalDependencies:
        #Add new table with functional dependency attributes and with the functional dependency itself
        newAttrs: set[FD.FunctionalDependency] = functionalDependency.determinants.union(functionalDependency.nonDeterminants)
        newTable: Table = Table(newAttrs, {functionalDependency})
        newTables.add(deepcopy(newTable))
    # make appropriate attributes prime
    for relation in newTables:
        for dependency in relation.functionalDependencies:
            for attr in dependency.determinants:
                attr.isPrime = True
                for a in relation.attributes:
                    if a.name == attr.name:
                        a.isPrime = True
                        relation.primaryKey.add(attr) # add attribute to table's PK
        primeAttributes: list[str] = [attr.name for attr in relation.attributes if attr.isPrime]
        newTableName: str = "".join(primeAttributes)
        if originalTable.name[:-1] in newTableName: # if new table has same PK as original table
            relation.name = originalTable.name
        else:
            relation.name = newTableName + 's'

    return newTables

def normalizeToBCNF(table: Table) -> set[Table]:
    if table.isBCNF():
        return {table}

    newTables: set[Table] = set()
    originalTable: Table = deepcopy(table)
    for functionalDependency in originalTable.functionalDependencies:
        # find the functional dependency that violates BCNF
        if not originalTable.isSuperkey(functionalDependency.determinants):
            # R-A in the form of X->A in Relation R
            # determine new attributes for R-A table
            origAttrNames: set[str] = set([attr.name for attr in originalTable.attributes])
            newAttrNames: set[set] = origAttrNames.difference(functionalDependency.getNonDeterminantNames()) # R - A
            newAttrs: set[A.Attribute] = set()
            for name in newAttrNames: # gets attribute objects based on names in newAttrNames
                if name in functionalDependency.getDeterminantNames(): # make X in X -> A a prime attribute in new table
                    for attribute in deepcopy(originalTable.attributes):
                        if name == attribute.name:
                            attribute.isPrime = True
                            newAttrs.add(attribute)
                else: # add other attributes to newAttrs list
                    for attribute in deepcopy(originalTable.attributes):
                        if name == attribute.name:
                            newAttrs.add(attribute)
            newFunctionalDependency = FD.FunctionalDependency(newAttrs, newAttrs)
            primeAttributes: list[str] = [a.name for a in newAttrs if a.isPrime]
            newTableName: str = "".join(primeAttributes)
            if originalTable.name[:-1] in newTableName:
                newTableName = originalTable.name[:-1]
            newTable = deepcopy(Table(newAttrs, {newFunctionalDependency}, newTableName + 's'))
            # define new primary key
            newTable.primaryKey = newTable.getPrimeAttributes()
            """for dependency in newTable.functionalDependencies:
                if dependency.determinants == dependency.nonDeterminants:
                    for attr in dependency.determinants:
                        attr.isPrime = True"""
            newTables.add(newTable)

            #XA in the form of X->A in Relation R
            newAttrs = functionalDependency.determinants.union(functionalDependency.nonDeterminants)
            for attr in newAttrs: # update attribute's prime status
                if attr.name in functionalDependency.getDeterminantNames():
                    attr.isPrime = True
                elif attr.name in functionalDependency.getNonDeterminantNames():
                    attr.isPrime = False
            primeAttributes: list[str] = [a.name for a in newAttrs if a.isPrime]
            newTableName: str = "".join(primeAttributes)
            if originalTable.name[:-1] in newTableName:
                newTableName = originalTable.name[:-1]
            newTable = deepcopy(Table(newAttrs, {functionalDependency}, newTableName + 's'))
            newTable.primaryKey = newTable.getPrimeAttributes() # update PK for table XA
            for dependency in newTable.functionalDependencies: # update FDs
                for attr in dependency.determinants:
                    if attr.name in [key.name for key in newTable.primaryKey]:
                        attr.isPrime = True
                for attr in dependency.nonDeterminants:
                    if attr.name not in [key.name for key in newTable.primaryKey]:
                        attr.isPrime = False
            newTables.add(newTable)
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