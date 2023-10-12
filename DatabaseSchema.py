# basically just a list of tables (needs to be changed to tables)
import Table as T

class DatabaseSchema:
    functionalDependencies: list[T.Table]
    
    def __init__(self, functionalDependencies: list[T.Table]) -> None:
        self.functionalDependencies = functionalDependencies
        
def normalizeTo1NF(databaseSchema: DatabaseSchema) -> list[DatabaseSchema]:
    normalizedDatabaseSchema: list[DatabaseSchema] = []
    for functionalDependency in databaseSchema:
        normalizedDatabaseSchema.append(T.normalizeTo1NF(functionalDependency))
    return normalizedDatabaseSchema

def normalizeTo2NF(databaseSchema: DatabaseSchema) -> list[DatabaseSchema]:
    return None

def normalizeTo3NF(databaseSchema: DatabaseSchema) -> list[DatabaseSchema]:
    return None

def normalizeToBCNF(databaseSchema: DatabaseSchema) -> list[DatabaseSchema]:
    return None
