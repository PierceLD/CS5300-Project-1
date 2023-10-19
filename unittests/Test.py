import unittest

class Test(unittest.TestCase):
    
    set0: set[int] = set([0, 1, 2, 3])
    set1: set[int] = set([1, 2])
    
    def test(self) -> None:
        for i in self.set1:
            self.assertTrue(i in self.set0)