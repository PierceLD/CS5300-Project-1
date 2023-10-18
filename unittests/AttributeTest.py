import unittest
import Attribute as A

class AttributeTest(unittest.TestCase):
    
    attribute1: A.Attribute = A.Attribute("list", False, "LIST")
    attribute2: A.Attribute = A.Attribute("ssn", True, "INT")
    attribute3: A.Attribute = A.Attribute("varchar_variable", True, "VARCHAR")
    
    def testConstructor(self) -> None:
        self.assertEqual(self.attribute1.name, "list")
        self.assertEqual(self.attribute2.name, "ssn")
        self.assertEqual(self.attribute3.name, "varchar_variable")
    
        self.assertFalse(self.attribute1.isPrime)
        self.assertTrue(self.attribute2.isPrime)
        self.assertTrue(self.attribute3.isPrime)
    
        self.assertEqual(self.attribute1.dataType, "LIST")
        self.assertEqual(self.attribute2.dataType, "INT")
        self.assertEqual(self.attribute3.dataType, "VARCHAR")
        
    def testSet_isPrime(self) -> None:
        self.attribute1.set_isPrime(True)
        self.assertTrue(self.attribute1.isPrime)
        
        self.attribute1.set_isPrime(False)
        self.assertFalse(self.attribute1.isPrime)