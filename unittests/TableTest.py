import unittest
import Table as T
import FunctionalDependency as FD
import Attribute as A
import DatabaseSchema as DS

class TableTest(unittest.TestCase):
    
    listAttribute: A.Attribute = A.Attribute("list", True, True, "VARCHAR")
    
    notOneNFTable: T.Table = T.Table(set([listAttribute]), set([listAttribute]), set())
    
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
    myTable = T.Table(attributes=attrs, primaryKey=set([attrs[0]]), functionalDependencies=fds)
    
    def testIs1NF(self) -> None:
        self.assertEqual(self.notOneNFTable.is1NF(), False)
        self.assertEqual(self.myTable.is1NF(), True)
        
    def testIs2NF(self) -> None:
        self.assertEqual(self.notOneNFTable.is2NF(), False)
        self.assertEqual(self.myTable.is2NF(), False)
        
    def testNormalizeTo2NF(self) -> None:
        newTables: set[T.Table] = T.normalizeTo2NF(self.myTable)
        for table in newTables:
            print(table)
            self.assertEqual(table.is2NF(), True)
        
    def testNormalizeTo3NF(self) -> None:
        newTables: set[T.Table] = T.normalizeTo3NF(self.myTable)
        for table in newTables:
            print(table)
            self.assertEqual(table.is2NF(), True)
        
    def fullTest(self, originalTables: set[T.Table]) -> None:
        tables: set[T.Table] =  originalTables
        tables = self.normalize(tables, DS.NormalForm.oneNF)
        
    def normalize(self, tables: set[T.Table], normalForm: DS.NormalForm) -> T.Table:
        return normalForm.value(tables)
        
    def testPrint(self) -> None:
        print(self.notOneNFTable)
        print(self.myTable)
    
    