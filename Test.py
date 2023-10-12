#This class creates hard-coded attributes and functional dependencies and inputs them into a table for testing

import Table as table
import Attribute as attribute
import FunctionalDependency as FD






def main():
    
    attrs = [attribute.Attribute("SSN",isPrime=True),attribute.Attribute("Pnumber",isPrime=True),
             attribute.Attribute("Hours"),attribute.Attribute("Ename"),attribute.Attribute("Pname"),attribute.Attribute("Plocation")]
    fd1 = FD.FunctionalDependency({attrs[0],attrs[1]},{attrs[2]})
    fd2 = FD.FunctionalDependency({attrs[0]},{attrs[3]})
    fd3 = FD.FunctionalDependency({attrs[1]},{attrs[4], attrs[5]})
    fds = [fd1, fd2, fd3]
    myTable = table.Table(attributes=attrs, functionalDependencies=fds)

    print(myTable)
    
    normalized2nf = table.normalizeTo2NF(myTable)

    for ntable in normalized2nf:
        print(ntable)


if __name__ == '__main__':
    main()



