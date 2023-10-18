import unittest
import Table as T
import FunctionalDependency as FD
import Attribute as A

class TableTest(unittest.TestCase):
    
    listAttribute: A.Attribute = A.Attribute("list", True, "LIST")
    
    notOneNFTable: T.Table = T.Table(set([listAttribute]), set())
    
    oneNFTable: T.Table = T.Table(set([]))
    
    def testIs1NF(self) -> None:
        self.assertEqual(self.notOneNFTable.is1NF(), False)
        
    