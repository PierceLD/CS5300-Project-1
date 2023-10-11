import DatabaseSchema
import FunctionalDependency
import Attribute

name: Attribute.Attribute = Attribute.Attribute("name")
age: Attribute.Attribute = Attribute.Attribute("age")
primeAttributes: list[Attribute.Attribute] = [name]
nonPrimeAttributes: list[Attribute.Attribute] = [name]
functionalDependency: FunctionalDependency.FunctionalDependency = FunctionalDependency.FunctionalDependency(primeAttributes, nonPrimeAttributes)
print(name)
print(functionalDependency)