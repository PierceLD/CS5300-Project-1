# basically just a list of tables (needs to be changed to tables)
import Table as T

class DatabaseSchema:
    functionalDependencies: list[T.Table]
    
    def __init__(self, functionalDependencies: list[T.Table]) -> None:
        self.functionalDependencies = functionalDependencies
        
def normalizeToNF1(databaseSchema: DatabaseSchema) -> list[DatabaseSchema]:
    normalizedDatabaseSchema: list[DatabaseSchema] = []
    for functionalDependency in databaseSchema:
        normalizedDatabaseSchema.append(T.normalizeToNF1(functionalDependency))
    return normalizedDatabaseSchema

def normalizeToNF2(databaseSchema: DatabaseSchema) -> list[DatabaseSchema]:
    return None

def normalizeToNF3(databaseSchema: DatabaseSchema) -> list[DatabaseSchema]:
    return None

def normalizeToBCNF(databaseSchema: DatabaseSchema) -> list[DatabaseSchema]:
    return None
