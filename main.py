import DatabaseSchema
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
    key_set = P.keyParse(key)

    # get functional dependencies and parse determinants and dependents
    print("Input Functional Dependencies (type “exit” and hit enter to complete your dependency list):")
    fd: str = ""
    fd_list: list[str] = [] # list of inputted fds
    parsed_fd_list: list[FD.FunctionalDependency] = [] # list of parsed fds
    while fd != "exit":
        fd = input()
        fd_list.append(fd)
    parsed_fd_list = P.fdParse(fd_list, key_set) # list of FDs used to create Table object

    # create the Table object with Attributes and FDs
    table: T.Table = T.Table(attributes, parsed_fd_list)

    print("Choice of the highest normal form to reach (1: 1NF, 2: 2NF, 3: 3NF, B: BCNF, 4: 4NF, 5: 5NF):")
    highest_nf: int = int(input())

    print("Find the highest normal form of the input table? (1: Yes, 2: No):")
    find_hnf: int = int(input())