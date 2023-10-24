#This class creates hard-coded attributes and functional dependencies and inputs them into a table for testing

import Table as table
import Attribute as attribute
import FunctionalDependency as FD






def main():
    #3NF test attributes and fds
    # attrs = [attribute.Attribute("SSN",isPrime=True),attribute.Attribute("Ename"),
    #          attribute.Attribute("Bdate"),attribute.Attribute("Address"),attribute.Attribute("Dnumber"),
    #          attribute.Attribute("Dname"),attribute.Attribute("DnumberSSN")]
    # fd1 = FD.FunctionalDependency({attrs[0]}, {attrs[1], attrs[2], attrs[3], attrs[4]})
    # fd2 = FD.FunctionalDependency({attrs[4]}, {attrs[5], attrs[6]})
    # fds = [fd1, fd2]
    # myTable = table.Table(attributes=set(attrs), functionalDependencies=fds)

    #BCNF test attributes and fds
    attrs = [attribute.Attribute("StudID",isPrime=True),attribute.Attribute("Course", isPrime=True),
             attribute.Attribute("Instructor")]
    fd1 = FD.FunctionalDependency({attrs[0], attrs[1]}, {attrs[2]})
    fd2 = FD.FunctionalDependency({attrs[2]}, {attrs[1]})
    fds = {fd1, fd2}
    myTable = table.Table(attributes=set(attrs), functionalDependencies=fds)


    print(myTable)
    
    
    print("Is the table in bcnf?",myTable.isBCNF())

    normalized = table.normalizeToBCNF(myTable)

    for r in normalized:
        print(r)
        # for a in r.attributes:
        #     print(a, a.isPrime)
        print(r.isBCNF())
        

if __name__ == '__main__':
    main()



