from copy import deepcopy, copy
import Attribute as A
import FunctionalDependency as FD
import DataTable as DT

class Table:
    name: str
    attributes: set[A.Attribute]
    primaryKey: set[A.Attribute]
    functionalDependencies: set[FD.FunctionalDependency]
    dataTuples: list[dict[str, list[str]]]
    dataTable: DT.DataTable
    
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
            if (not functionalDependency.isMultiValued) and (functionalDependency.determinants < self.primaryKey): # if any of the determinants are a proper subset of the primary key (indicates partial FD)
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
    
    """ Assumptions:
        a table with 1 or 2 attributes is in 5NF
        a table with more than 5 attributes is not in 5NF
        a table is in 5NF if it has a least one attribute that is not part of the primary key
    """
    def is5NF(self) -> bool:
        self.makeDataTable()
        if not self.is4NF():
            return False
        if len(self.attributes) < 3:
            return True
        if len(self.attributes) > 3:
            return False
        for attribute in self.attributes:
            if not attribute.isPrime:
                return True
        if len(self.attributes) == 3:
            dataTables: list[DT.DataTable] = []
            for attribute in self.attributes:
                dataTables.append(self.dataTable.project(self.attributes.difference(set({attribute}))))
            testJoinOne: DT.DataTable = DT.reduce(dataTables[0].equalJoin(dataTables[0].attributeSet.intersection(dataTables[1].attributeSet), dataTables[1]))
            testJoinTwo: DT.DataTable = DT.reduce(dataTables[1].equalJoin(dataTables[1].attributeSet.intersection(dataTables[2].attributeSet), dataTables[2]))
            testJoinTable: DT.DataTable = DT.reduce(testJoinOne.equalJoin(testJoinOne.attributeSet.intersection(testJoinTwo.attributeSet), testJoinTwo))
            if testJoinTable.equal(self.dataTable):
                return False
            # for table in dataTables:
            #     # print(table)
            #     for joinTable in dataTables:
            #         if table is joinTable:
            #             continue
            #         testJoinOne: DT.DataTable = DT.reduce(table.equalJoin(table.attributeSet.intersection(joinTable.attributeSet), joinTable))
            #         testJoinTable: DT.DataTable = DT.reduce(table.equalJoin(table.attributeSet.intersection(joinTable.attributeSet), joinTable))
            #         testJoinTable: DT.DataTable = DT.reduce(table.equalJoin(table.attributeSet.intersection(joinTable.attributeSet), joinTable))
            #         print(len(testJoinTable.rowList))
            #         # print(testJoinTable)
            #         # print(testJoinTable.equal(self.dataTable))
            #         if testJoinTable.equal(self.dataTable):
            #             return False
        return True
    
    def setName(self) -> None:
        newName: str = ""
        for attribute in self.getPrimeAttributes():
            newName += attribute.name + " "
        self.name = newName
            
    def makeDataTable(self) -> None:
        newDataTable: DT.DataTable = DT.DataTable(self.attributes, [])
        for dictionary in self.dataTuples:
            newDictionary: dict[A.Attribute, str] = {}
            for attribute in self.attributes:
                newDictionary[attribute] = dictionary[attribute.name][0]
            newDataTable.addRow(DT.Row(newDataTable, newDictionary))
        self.dataTable = newDataTable
    
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

        attr_list: list[A.Attribute] = [attr for attr in self.attributes]
        max_name_length = max(len(attr.name) for attr in attr_list)

        for tuple in self.dataTuples:
            for attr in attr_list:
                if len(tuple[attr.name][0]) > max_name_length:
                    max_name_length = len(tuple[attr.name][0])

        total_width = (max_name_length + 4) * len(attr_list) + 10
        border = "+" + "-" * (total_width - 2) + "+\n"
        result = border

        names = " | ".join([f"{'(PK)' if attr.isPrime else ''}{attr.name:{max_name_length}}" for attr in attr_list])
        result += f"| {names:{total_width - 4}} |\n"  # Adjusted alignment and spacing
        result += border

        for tuple in self.dataTuples:
            values = " | ".join([f"{tuple[attr.name][0]:{max_name_length}}" for attr in attr_list])
            result += f"| {values:{total_width - 4}} |\n"  # Adjusted alignment and spacing
            result += border

        result += "Functional Dependencies:\n"
        for fd in self.functionalDependencies:
            result += "\t" + fd.__str__() + "\n"
        return result


""" This function will put the correct projections of data
    from the original input table's data tuples into all of
    the new decomposed relations.
    Input: the original data tuples, a set decomposed/altered relations
    Output: None, modifies each table in newTables in-place
"""
def projectData(originalTuples: list[dict[str,list[str]]], newTables: set[Table]) -> None:
    for table in newTables:
        newDataTuples: list[dict[str,list[str]]] = []
        for tuple in originalTuples:
            newTuple: dict[str,list[str]] = dict()
            for attr in table.attributes:
                newTuple[attr.name] = copy(tuple[attr.name])
            if newTuple not in newDataTuples: # if not already in new list of tuples (removes duplicates)
                newDataTuples.append(newTuple)
        table.dataTuples = copy(newDataTuples)
    return

""" Helper function to make any attribute in a FD reference an
    Attribute object in the list of table's attributes
    Input: Table
    Output: None"""
def makeFDReferenceAttributes(table: Table) -> None:
    for functionalDependency in table.functionalDependencies:
            for determinant in functionalDependency.determinants:
                for attr in table.attributes:
                    if determinant.name == attr.name:
                        determinant = attr
            for nonDeterminant in functionalDependency.nonDeterminants:
                for attr in table.attributes:
                    if nonDeterminant.name == attr.name:
                        nonDeterminant = attr
    return


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
            # update original FDs so that newly prime attribute is removed from any non-determinant (i.e. if original PK determined original multi-valued attribute)
            fdsToRemove: set[FD.FunctionalDependency] = set()
            for fd in [dependency for dependency in newTable.functionalDependencies if not dependency.isMultiValued]:
                if (attribute in fd.nonDeterminants) and (len(fd.nonDeterminants) > 1): # if non-determinant is not just the attribute, only remove the attribute
                    fd.nonDeterminants.remove(attribute)
                elif {attribute} == fd.nonDeterminants: # if non-determinant is only the newly prime attribute
                    fdsToRemove.add(fd)
            for fd in fdsToRemove: # remove old fd from table, if any
                newTable.functionalDependencies.remove(fd)
            # add a multi-valued FD to the table, in case 4NF wants to be reached
            originalPK: set[A.Attribute] = set() 
            for old_key in table.primaryKey: # get old primary key
                for new_key in newTable.primaryKey:
                    if new_key.name == old_key.name:
                        originalPK.add(new_key)
            addNewMVFD: bool = True
            newMVFD: FD.FunctionalDependency = FD.FunctionalDependency(originalPK, {attribute}, isMultiValued=True)
            for fd in newTable.functionalDependencies: # check if MVFD is already in set of FDs, then don't add a new one
                if newMVFD.determinants == fd.determinants and newMVFD.nonDeterminants == fd.nonDeterminants:
                    addNewMVFD = False
            if addNewMVFD:
                newTable.functionalDependencies.add(newMVFD) # make original PK determine new attribute

    # add a trivial FD to the new table
    newTable.functionalDependencies.add(FD.FunctionalDependency(newTable.primaryKey, newTable.primaryKey))

    # update name if necessary (more attributes added to PK)
    if len(newTable.primaryKey) > len(table.primaryKey):
        primeAttributeNames: list[str] = [attr.name for attr in newTable.primaryKey]
        newTableName: str = "".join(primeAttributeNames)
        newTable.name = newTableName + 's'
    
    # create new data tuples
    originalDataTuples: list[dict[str,list[str]]] = copy(table.dataTuples)
    for attr in newTable.getPrimeAttributes():
        if attr.name not in [attr.name for attr in table.getPrimeAttributes()]: # if attr wasn't originally in primary key
            prev_length: int = len(originalDataTuples)
            for t in range(prev_length): # go thru original table's data tuples
                try:
                    attr_val: list[str] = originalDataTuples[t][attr.name+'s']
                except:
                    attr_val = originalDataTuples[t][attr.name]
                for value in attr_val: # since attribute name became singular, need to make it plural
                    newTuple: dict[str,list[str]] = copy(originalDataTuples[t])
                    try:
                        newTuple.pop(attr.name+'s') # remove old attribute's key value pair
                    except:
                        newTuple.pop(attr.name)
                    newTuple[attr.name] = [value] # add new attribute's key value pair
                    originalDataTuples.append(newTuple)
            originalDataTuples = originalDataTuples[prev_length:] # editing list in-place so need to use indexing and splicing to get correct tuples
    newTable.dataTuples = copy(originalDataTuples)

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
        """for functionalDependency in newTable.functionalDependencies:
            for determinant in functionalDependency.determinants:
                for attr in newTable.attributes:
                    if determinant.name == attr.name:
                        determinant = attr
            for nonDeterminant in functionalDependency.nonDeterminants:
                for attr in newTable.attributes:
                    if nonDeterminant.name == attr.name:
                        nonDeterminant = attr"""
        makeFDReferenceAttributes(newTable)

    # project original data into new tables
    projectData(table.dataTuples, newTables)

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
        """for functionalDependency in newTable.functionalDependencies:
            for determinant in functionalDependency.determinants:
                for attr in newTable.attributes:
                    if determinant.name == attr.name:
                        determinant = attr
            for nonDeterminant in functionalDependency.nonDeterminants:
                for attr in newTable.attributes:
                    if nonDeterminant.name == attr.name:
                        nonDeterminant = attr"""
        makeFDReferenceAttributes(newTable)

    # project original data into new tables
    projectData(table.dataTuples, newTables)

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
            newFunctionalDependency: FD.FunctionalDependency = FD.FunctionalDependency(newAttrs, newAttrs) # adds a new trivial FD to R-A table
            primeAttributes: list[str] = [a.name for a in newAttrs if a.isPrime]
            newTableName: str = "".join(primeAttributes)
            newTable = deepcopy(Table(newAttrs, {newFunctionalDependency}, newTableName + 's'))
            newTables.add(newTable)

            #XA in the form of X->A in Relation R
            newAttrs = deepcopy(functionalDependency.determinants.union(functionalDependency.nonDeterminants))
            for attr in newAttrs: # update each attribute's prime status
                for determinant in functionalDependency.determinants:
                    if attr.name == determinant.name:
                        attr.isPrime = True
                for nonDeterminant in functionalDependency.nonDeterminants:
                    if attr.name == nonDeterminant.name:
                        attr.isPrime = False
            primeAttributes: list[str] = [a.name for a in newAttrs if a.isPrime]
            newTableName: str = "".join(primeAttributes)
            newTable = deepcopy(Table(newAttrs, {functionalDependency}, newTableName + 's'))

            """for dependency in newTable.functionalDependencies: # update FDs
                for determinant in dependency.determinants:
                    for attr in newTable.attributes:
                        if determinant.name == attr.name:
                            determinant = attr
                for nonDeterminant in dependency.nonDeterminants:
                    for attr in newTable.attributes:
                        if nonDeterminant.name == attr.name:
                            nonDeterminant = attr"""
            makeFDReferenceAttributes(newTable)
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

    # project original data into new tables
    projectData(table.dataTuples, newTables)

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
            newFunctionalDependency: set[FD.FunctionalDependency] = {FD.FunctionalDependency(functionalDependency.determinants, functionalDependency.nonDeterminants, True)}
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
    
    # add any normal dependencies to appropriate new table, if it still holds for the new table's attributes
    for newTable in newTables:
        table_attr_names: set[str] = set([a.name for a in newTable.attributes])
        for fd in nonMultiValuedDependencies:
            fd_attrs: set[A.Attribute] = fd.determinants.union(fd.nonDeterminants)
            fd_attr_names: set[str] = set([attr.name for attr in fd_attrs])
            if fd_attr_names <= table_attr_names: # add the fd if the union of it's determinant and non-determinant is a subset of the new table's attributes
                newTable.functionalDependencies.add(fd)  
    
    # make sure attributes in all FDs are referencing an attribute in newTable.attributes list
    for newTable in newTables:
        """for functionalDependency in newTable.functionalDependencies:
            for determinant in functionalDependency.determinants:
                for attr in newTable.attributes:
                    if determinant.name == attr.name:
                        determinant = attr
            for nonDeterminant in functionalDependency.nonDeterminants:
                for attr in newTable.attributes:
                    if nonDeterminant.name == attr.name:
                        nonDeterminant = attr"""
        makeFDReferenceAttributes(newTable)

    # project original data into new tables
    projectData(table.dataTuples, newTables)

    return newTables
    
def normalizeTo5NF(table: Table) -> set[Table]:
    if table.is5NF():
        return {table}
<<<<<<< HEAD
    if len(table.attributes) > 3:
        print("this can not be decomposed")
        return {table}
    table.makeDataTable()
    newTables: set[Table] = set()
    # dataTables: list[DT.DataTable] = []
    for attribute in table.attributes:
        # dataTables.append(table.dataTable.project(table.attributes.difference(set({attribute}))))
        newAttributes: set[A.Attribute] = deepcopy(table.attributes.difference(set({attribute})))
        newFunctionalDependency: set[FD.FunctionalDependency] = set({FD.FunctionalDependency(newAttributes, newAttributes)})
        newTable: Table = Table(attributes=newAttributes, functionalDependencies=newFunctionalDependency)
        newTable.setName()
        newTables.add(newTable)
    return newTables
=======
    
>>>>>>> 87187f0a496300159f810f7dac2e406c23015436
