import DatabaseSchema as D
import FunctionalDependency as FD
import Attribute as A
import Parse as P
import Table as T
"""
name: Attribute.Attribute = Attribute.Attribute("name")
age: Attribute.Attribute = Attribute.Attribute("age")
primeAttributes: list[Attribute.Attribute] = [name]
nonPrimeAttributes: list[Attribute.Attribute] = [name]
functionalDependency: FunctionalDependency.FunctionalDependency = FunctionalDependency.FunctionalDependency(primeAttributes, nonPrimeAttributes)
print(name)
print(functionalDependency)
"""
if __name__ == "__main__":

    # get input data file and parse data to get attributes
    print("Input dataset:")
    file: str = input()
    attributes: list[A.Attribute] = P.csvParse(file) # list of Attributes used to create Table object

    # get Primary Key of table
    print("Key (can be composite):")
    key: str = input()
    key_set: set[str] = P.keyParse(key)

    # set isPrime to true for any attribute in the primary key
    for attr in attributes:
        if attr.name in key_set:
            attr.isPrime = True

    # get functional dependencies and parse determinants and dependents
    print("Input Functional Dependencies (type “exit” and hit enter to complete your dependency list):")
    fd: str = ""
    fd_list: list[str] = [] # list of inputted fds
    parsed_fd_list: list[FD.FunctionalDependency] = [] # list of parsed fds
    while fd != "exit":
        fd = input()
        if fd != "exit":
            fd_list.append(fd)
    print(fd_list)
    parsed_fd_list = P.fdParse(fd_list, key_set) # list of FDs used to create Table object

    # create the Table object with Attributes and FDs
    table: T.Table = T.Table(attributes, parsed_fd_list)
    # create DatabaseSchema object and add the table to it
    DB_schema: D.DatabaseSchema = D.DatabaseSchema(table)
    print(table)
    
    oneNFTable: T.Table = T.normalizeTo1NF(table)
    print(oneNFTable)

    # normalizing the DB schema
    print("Choice of the highest normal form to reach (1: 1NF, 2: 2NF, 3: 3NF, B: BCNF, 4: 4NF, 5: 5NF):")
    nf_to_reach: str = input()
    DB_schema.normalize(nf_to_reach)

    print("Find the highest normal form of the input table? (1: Yes, 2: No):")
    find_hnf: str = input()
    if find_hnf == '1':
        DB_schema.findHighestNF()