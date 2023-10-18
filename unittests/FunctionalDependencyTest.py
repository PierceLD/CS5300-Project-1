import unittest
import Attribute as A
import FunctionalDependency as FD

class AttributeTest(unittest.TestCase):
    
    attribute0: A.Attribute = A.Attribute("list", False, "LIST")
    attribute1: A.Attribute = A.Attribute("ssn", True, "INT")
    attribute2: A.Attribute = A.Attribute("varchar_variable", True, "VARCHAR")
    
    attributes: set[A.Attribute] = set([attribute0, attribute1, attribute2])
    
    
    def testConstructor(self) -> None:
        functionalDependency: FD.FunctionalDependency = FD.FunctionalDependency(self.attributes, self.attributes)
        self.assertEqual(len(functionalDependency.determinants), 3)
        self.assertEqual(len(functionalDependency.nonDeterminants), 3)
        self.assertTrue(self.attribute0 in functionalDependency.determinants)
        self.assertTrue(self.attribute1 in functionalDependency.nonDeterminants)