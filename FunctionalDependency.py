# two lists of attributes
# one for the prime attributes and one for the non-prime attributes
import Attribute

class FunctionalDependency:
    primeAttributes: list[Attribute.Attribute]
    nonPrimeAttributes: list[Attribute.Attribute]
    
    def __init__(self, primeAttributes: list[Attribute.Attribute], nonPrimeAttributes: list[Attribute.Attribute]) -> None:
        self.primeAttributes = primeAttributes
        self.nonPrimeAttributes = nonPrimeAttributes
        
    def __str__(self) -> str:
        returnString: str = "{ "
        for primeAttribute in self.primeAttributes:
            returnString += primeAttribute.__str__() + ", "
        returnString += "} -> { "
        for nonPrimeAttribute in self.nonPrimeAttributes:
            returnString += nonPrimeAttribute.__str__() + ", "
        returnString += "}"
        return returnString


