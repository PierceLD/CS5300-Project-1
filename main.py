import DatabaseSchema
import FunctionalDependency
import Attribute
import Parse

name: Attribute.Attribute = Attribute.Attribute("name")
age: Attribute.Attribute = Attribute.Attribute("age")
primeAttributes: list[Attribute.Attribute] = [name]
nonPrimeAttributes: list[Attribute.Attribute] = [name]
functionalDependency: FunctionalDependency.FunctionalDependency = FunctionalDependency.FunctionalDependency(primeAttributes, nonPrimeAttributes)
print(name)
print(functionalDependency)

if __name__ == "__main__":
    #get input data file and parse data
    print("Input dataset:")
    file: str = input()

    print("Input Functional Dependencies (type “exit” and hit enter to complete your dependency list):")
    fd: str = ""
    while fd != "exit":
        fd = input()

    print("Choice of the highest normal form to reach (1: 1NF, 2: 2NF, 3: 3NF, B: BCNF, 4: 4NF, 5: 5NF):")
    highest_nf: int = int(input())

    print("Find the highest normal form of the input table? (1: Yes, 2: No):")
    find_hnf: int = int(input())

    print("Key (can be composite):")
    key: str = input()