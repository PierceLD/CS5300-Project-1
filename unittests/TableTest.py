import unittest
import Table as T
import FunctionalDependency as FD
import Attribute as A

class TableTest(unittest.TestCase):
    
    listAttribute: A.Attribute = A.Attribute("list", True, "LIST")
    
    notOneNFTable: T.Table = T.Table(set([listAttribute]), set())
    
    # oneNFTable: T.Table = T.Table(set([]))
    
    def testIs1NF(self) -> None:
        self.assertEqual(self.notOneNFTable.is1NF(), False)
        
    def testIs2NF(self) -> None:
        self.assertEqual(self.notOneNFTable.is2NF(), False)
    
    attrs = [A.Attribute("SSN",isPrime=True),A.Attribute("Ename"),
        A.Attribute("Bdate"),A.Attribute("Address"),A.Attribute("Dnumber"),
        A.Attribute("Dname"),A.Attribute("DnumberSSN")]
    fd1 = FD.FunctionalDependency({attrs[0]}, {attrs[1], attrs[2], attrs[3], attrs[4]})
    fd2 = FD.FunctionalDependency({attrs[4]}, {attrs[5], attrs[6]})
    fds = [fd1, fd2]
    myTable = T.Table(attributes=attrs, functionalDependencies=fds)
    