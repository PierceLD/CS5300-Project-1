#This class creates hard-coded attributes and functional dependencies and inputs them into a table for testing

import Table as table
import Attribute as attribute
import FunctionalDependency as FD






def main():
    
    attrs = [attribute.Attribute("SSN",isPrime=True),attribute.Attribute("Ename"),
             attribute.Attribute("Bdate"),attribute.Attribute("Address"),attribute.Attribute("Dnumber"),
             attribute.Attribute("Dname"),attribute.Attribute("DnumberSSN")]
    fd1 = FD.FunctionalDependency({attrs[0]}, {attrs[1], attrs[2], attrs[3], attrs[4]})
    fd2 = FD.FunctionalDependency({attrs[4]}, {attrs[5], attrs[6]})
    fds = [fd1, fd2]
    myTable = table.Table(attributes=attrs, functionalDependencies=fds)

    print(myTable)
    
    
    print("Is the table in bcnf?",myTable.isBCNF())

    normalized = table.normalizeTo3NF(myTable)

    for r in normalized:
        print(r)
        
        print("","is 3nf?" , r.is3NF())

if __name__ == '__main__':
    main()



