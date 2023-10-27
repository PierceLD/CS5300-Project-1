# basically a list of attributes and functional dependencies
from copy import deepcopy
import Attribute as A
import FunctionalDependency as FD

class Table:
    name: str
    attributes: set[A.Attribute]
    primaryKey: set[A.Attribute]
    functionalDependencies: set[FD.FunctionalDependency]
    dataTuples: list[dict[str, list[str]]]
    
    def __init__(self, attributes: set[A.Attribute], functionalDependencies: set[FD.FunctionalDependency], name: str = "") -> None:
        self.attributes = attributes
        self.primaryKey = self.getPrimeAttributes()
        self.functionalDependencies = functionalDependencies
        self.name = name
        self.dataTuples = []
        
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
            if not functionalDependency.isMultiValued and functionalDependency.determinants < self.primaryKey: # if any of the determinants are a proper subset of the primary key (indicates partial FD)
                return False
        return True

    def is3NF(self) -> bool:
        if not self.is2NF():
            return False

        # check for each FD if determinant is a superkey or if dependent is a prime attribute
        for functionalDependency in self.functionalDependencies:
            if not functionalDependency.isMultiValued:
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
            if not functionalDependency.isMultiValued:
                if not self.isSuperkey(functionalDependency.determinants): # if the FD determinant is not a superkey, violates BCNF constraint
                    return False
        return True
    
    def is4NF(self) -> bool:
        if not self.isBCNF():
            return False
        for functionalDependency in self.functionalDependencies:
            if not self.isTrivialMultiValuedDependency(functionalDependency) and functionalDependency.isMultiValued:
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
        return functionalDependency.isMultiValued and (self.attributes is functionalDependency.determinants.union(functionalDependency.nonDeterminants))

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
        return {deepcopy(table)} # return deepcopy's of input table to avoid changing input table's data

    newTable: Table = deepcopy(table) # create a new copy of the table

    for attribute in newTable.attributes:
        if attribute.isMultiValued:
            attribute.isPrime = True # make the attribute a key value and not multi-valued
            attribute.isMultiValued = False
            if attribute.name[-1] == 's': # make it singular if it's plural
                attribute.name = attribute.name[:-1]
            newTable.primaryKey.add(attribute) # add the attribute to the table's primary key
    # add a trivial FD to the new table
    newTable.functionalDependencies.add(FD.FunctionalDependency(newTable.primaryKey, newTable.primaryKey))
    # update name if necessary (more attributes added to PK)
    if len(newTable.primaryKey) > len(table.primaryKey):
        primeAttributeNames: list[str] = [attr.name for attr in newTable.primaryKey]
        newTableName: str = "".join(primeAttributeNames)
        newTable.name = newTableName + 's'

    return {newTable}

def normalizeTo2NF(table: Table) -> set[Table]:
    if table.is2NF():
        return {deepcopy(table)}
    
    newTables: set[Table] = set()
    originalTable: Table = deepcopy(table)
    # go thru FDs to find full FDs, where determinant = primary key, and partial FDs first
    for functionalDependency in originalTable.functionalDependencies:
        if not functionalDependency.isMultiValued:
            if functionalDependency.determinants.issubset(originalTable.primaryKey):
                newAttrs: set[A.Attribute] = functionalDependency.determinants.union(functionalDependency.nonDeterminants)
                newTable: Table = Table(newAttrs, {functionalDependency})
                if newTable.primaryKey == originalTable.primaryKey: # if PK of new table is same as original table, then give it the same name
                    newTable.name = originalTable.name
                else:
                    primeAttributeNames: list[str] = [attr.name for attr in newAttrs if attr.isPrime]
                    newTableName: str = "".join(primeAttributeNames)
                    newTable.name = newTableName + 's'
                newTables.add(deepcopy(newTable))

    # loop through FDs again to find transitive FDs, where determinant is not a subset of primary key
    for functionalDependency in originalTable.functionalDependencies:
        if not functionalDependency.isMultiValued:
            if functionalDependency.determinants.difference(originalTable.primaryKey) == functionalDependency.determinants: # if current FD determinant is not in primary key (indicating transitive FD)
                for newTable in newTables:
                    newFDs: set[FD.FunctionalDependency] = set()
                    for fd in newTable.functionalDependencies:
                        # if current FD determinant is in any of the newTable's FD non-determinants
                        if functionalDependency.getDeterminantNames().issubset(fd.getNonDeterminantNames()):
                            # add current FD to newTable FD list and add attributes newTable attribute list
                            newTable.attributes = newTable.attributes.union(functionalDependency.nonDeterminants)
                            newFDs.add(functionalDependency)
                    newTable.functionalDependencies = newTable.functionalDependencies.union(newFDs)

    # loop thru newTables to determine where to add multi-valued FDs, if any
    multivaluedFDs: set[FD.FunctionalDependency] = set([fd for fd in originalTable.functionalDependencies if fd.isMultiValued])
    if len(multivaluedFDs):
        for newTable in newTables:
            for fd in multivaluedFDs:
                fdAttrs: set[A.Attribute] = fd.determinants.union(fd.nonDeterminants)
                fdAttrNames: set[str] = set([attr.name for attr in fdAttrs])
                if fdAttrNames <= set([attr.name for attr in newTable.attributes]): # if union of fd attributes is a subset of newTable's attributes
                    newTable.functionalDependencies.add(fd) # add MVFD to new table's FDs

    # make sure attributes in all FDs are referencing an attribute in newTable.attributes list
    for newTable in newTables:
        for functionalDependency in newTable.functionalDependencies:
            for determinant in functionalDependency.determinants:
                for attr in newTable.attributes:
                    if determinant.name == attr.name:
                        determinant = attr
            for nonDeterminant in functionalDependency.nonDeterminants:
                for attr in newTable.attributes:
                    if nonDeterminant.name == attr.name:
                        nonDeterminant = attr

    return newTables
        
def normalizeTo3NF(table: Table) -> set[Table]:
    if table.is3NF():
        return {deepcopy(table)}

    newTables: set[Table] = set()
    originalTable: Table = deepcopy(table)
    for functionalDependency in originalTable.functionalDependencies:
        if not functionalDependency.isMultiValued:
            #Add new table with functional dependency attributes and with the functional dependency itself
            newAttrs: set[FD.FunctionalDependency] = functionalDependency.determinants.union(functionalDependency.nonDeterminants)
            newTable: Table = Table(newAttrs, {functionalDependency})
            newTables.add(deepcopy(newTable))
    # make appropriate attributes prime
    for relation in newTables:
        for dependency in relation.functionalDependencies:
            for d_attr in dependency.determinants:
                for attr in relation.attributes:
                    if d_attr.name == attr.name:
                        attr.isPrime = True # make attribute on lhs of dependency prime in relation's attribute set
                        d_attr = attr # make the attribute in determinant reference attribute in relation's attribute's set
                        relation.primaryKey.add(attr) # add attribute to table's PK
        primeAttributes: list[str] = [attr.name for attr in relation.attributes if attr.isPrime]
        newTableName: str = "".join(primeAttributes)
        relation.name = newTableName + 's'

    # loop thru newTables to determine where to add multi-valued FDs, if any
    multivaluedFDs: set[FD.FunctionalDependency] = set([fd for fd in originalTable.functionalDependencies if fd.isMultiValued])
    if len(multivaluedFDs):
        for newTable in newTables:
            for fd in multivaluedFDs:
                fdAttrs: set[A.Attribute] = fd.determinants.union(fd.nonDeterminants)
                fdAttrNames: set[str] = set([attr.name for attr in fdAttrs])
                if fdAttrNames <= set([attr.name for attr in newTable.attributes]): # if union of fd attributes is subset of the newTable's attributes
                    newTable.functionalDependencies.add(fd) # add MVFD to new table's FDs

    # make sure attributes in all FDs are referencing an attribute in newTable.attributes list
    for newTable in newTables:
        for functionalDependency in newTable.functionalDependencies:
            for determinant in functionalDependency.determinants:
                for attr in newTable.attributes:
                    if determinant.name == attr.name:
                        determinant = attr
            for nonDeterminant in functionalDependency.nonDeterminants:
                for attr in newTable.attributes:
                    if nonDeterminant.name == attr.name:
                        nonDeterminant = attr

    return newTables

def normalizeToBCNF(table: Table) -> set[Table]:
    if table.isBCNF():
        return {deepcopy(table)}

    newTables: set[Table] = set()
    originalTable: Table = deepcopy(table)
    for functionalDependency in originalTable.functionalDependencies:
        # find the functional dependency that violates BCNF, skip multi-valued dependencies
        if not originalTable.isSuperkey(functionalDependency.determinants) and not functionalDependency.isMultiValued:
            # R-A in the form of X->A in Relation R
            # determine new attributes for R-A table
            newAttrs: set[A.Attribute] = deepcopy(originalTable.attributes.difference(functionalDependency.nonDeterminants))
            for attr in newAttrs: # make attributes from X prime
                attr.isPrime = True
            newFunctionalDependency: FD.FunctionalDependency = FD.FunctionalDependency(newAttrs, newAttrs)
            primeAttributes: list[str] = [a.name for a in newAttrs if a.isPrime]
            newTableName: str = "".join(primeAttributes)
            newTable = deepcopy(Table(newAttrs, {newFunctionalDependency}, newTableName + 's'))
            newTables.add(newTable)

            #XA in the form of X->A in Relation R
            newAttrs = deepcopy(functionalDependency.determinants.union(functionalDependency.nonDeterminants))
            for attr in newAttrs: # update each attribute's prime status
                for determinant in functionalDependency.determinants:
                    if attr.name == determinant.name:
                        print("Determinant", attr)
                        attr.isPrime = True
                for nonDeterminant in functionalDependency.nonDeterminants:
                    if attr.name == nonDeterminant.name:
                        print("Non", attr)
                        attr.isPrime = False
            primeAttributes: list[str] = [a.name for a in newAttrs if a.isPrime]
            newTableName: str = "".join(primeAttributes)
            newTable = deepcopy(Table(newAttrs, {functionalDependency}, newTableName + 's'))

            for dependency in newTable.functionalDependencies: # update FDs
                for determinant in dependency.determinants:
                    for attr in newTable.attributes:
                        if determinant.name == attr.name:
                            determinant = attr
                for nonDeterminant in dependency.nonDeterminants:
                    for attr in newTable.attributes:
                        if nonDeterminant.name == attr.name:
                            nonDeterminant = attr
            newTables.add(newTable)

    # loop thru newTables to determine where to add multi-valued FDs, if any
    multivaluedFDs: set[FD.FunctionalDependency] = set([fd for fd in originalTable.functionalDependencies if fd.isMultiValued])
    if len(multivaluedFDs):
        for newTable in newTables:
            for fd in multivaluedFDs:
                fdAttrs: set[A.Attribute] = fd.determinants.union(fd.nonDeterminants)
                fdAttrNames: set[str] = set([attr.name for attr in fdAttrs])
                if fdAttrNames <= set([attr.name for attr in newTable.attributes]): # if union of fd attributes is subset of the newTable's attributes
                    newTable.functionalDependencies.add(fd) # add MVFD to new table's FDs

    return newTables

def normalizeTo4NF(table: Table) -> set[Table]:
    if table.is4NF():
        return {table}
    newTables: set[Table] = set()
    removedAttributes: set[A.Attribute] = set()
    nonMultiValuedDependencies: set[FD.FunctionalDependency] = set()
    for functionalDependency in table.functionalDependencies:
        if functionalDependency.isMultiValued and not table.isTrivialMultiValuedDependency(functionalDependency):
            #create new table that is trivial
            newAttributes: set[A.Attribute] = deepcopy(functionalDependency.determinants.union(functionalDependency.nonDeterminants))
            for attribute in newAttributes:
                attribute.isPrime = True
            removedAttributes.update(functionalDependency.nonDeterminants)
            newFunctionalDependency: set[FD.FunctionalDependency] = {FD.FunctionalDependency(newAttributes, newAttributes, True)}
            primeAttributes: list[str] = [a.name for a in newAttributes if a.isPrime]
            newTableName: str = "".join(primeAttributes)
            newTable: Table =  Table(newAttributes, newFunctionalDependency, newTableName + 's')
            newTables.add(newTable)
        else:
            nonMultiValuedDependencies.add(functionalDependency)
            
    # make a new table that has all the removed attributes, TODO: i don't think this is necessary since input table is going to be split
    """newAttributes: set[A.Attribute] = deepcopy(table.attributes.difference(removedAttributes))
    newFunctionalDependencies: set[FD.FunctionalDependency] = deepcopy(nonMultiValuedDependencies)
    newBaseTable: Table = Table(newAttributes, newFunctionalDependencies) # TODO i think this might be empty
    if len(newFunctionalDependencies) > 0:
        newTables.add(newBaseTable)"""
    return newTables
    
def normalizeTo5NF(table: Table) -> set[Table]:
    if table.is5NF():
        return {table}