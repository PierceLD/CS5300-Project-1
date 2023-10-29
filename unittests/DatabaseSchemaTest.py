import unittest
import Table as T
import FunctionalDependency as FD
import Attribute as A
import DatabaseSchema as DS

class DatabaseSchemaTest(unittest.TestCase):
    
    listAttribute: A.Attribute = A.Attribute("list", True, True, "VARCHAR")
    
    notOneNFTable: T.Table = T.Table(set([listAttribute]), set([listAttribute]), "Table with one attribute")
    
    # oneNFTable: T.Table = T.Table(set([]))
    
    
    attrs = [A.Attribute("SSN",isPrime=True),
            A.Attribute("Ename"),
            A.Attribute("Bdate"),
            A.Attribute("Address"),
            A.Attribute("Dnumber"),
            A.Attribute("Dname"),
            A.Attribute("DnumberSSN")]
    fd1 = FD.FunctionalDependency({attrs[0]}, {attrs[1], attrs[2], attrs[3], attrs[4]})
    fd2 = FD.FunctionalDependency({attrs[4]}, {attrs[5], attrs[6]})
    fds = [fd1, fd2]
    myTable = T.Table(attributes=attrs, functionalDependencies=fds, name="Student")

    ename = A.Attribute("Ename", isPrime=True)
    pname = A.Attribute("Pname", isPrime=True)
    dname = A.Attribute("Dname", isPrime=True)
    
    attributes: set[A.Attribute] = set()
    attributes.add(ename)
    attributes.add(pname)
    attributes.add(dname)
    functionalDependencies: set[FD.FunctionalDependency] = set()
    functionalDependencies.add(FD.FunctionalDependency({ename}, {pname}, isMultiValued=True))
    functionalDependencies.add(FD.FunctionalDependency({ename}, {dname}, isMultiValued=True))
    
    fourNFTestTable = T.Table(attributes, functionalDependencies, "Projects")
    
    def testMakeSvg(self) -> None:
        databaseSchema: DS.DatabaseSchema = DS.DatabaseSchema([self.fourNFTestTable, self.notOneNFTable, self.myTable])
        databaseSchema.makeSvg()