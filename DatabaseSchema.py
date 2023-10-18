# basically just a list of tables (needs to be changed to tables)
import Table as T

class DatabaseSchema:
    original_table: T.Table
    tables: list[T.Table]
    
    def __init__(self, original_table: T.Table, tables: list[T.Table] = []) -> None:
        self.original_table = original_table
        self.tables = tables.append(self.original_table) # add og input table to list of tables

    """ General method to normalize all tables in the schema in-place
        to specified normal form; calls each normalization function for entire DB schema
        Input: Normal form to achieve
        Output: None
    """
    def normalize(self, normal_form: str) -> None:
        if normal_form == '1':
            self.tables = normalizeTo1NF(self)
        elif normal_form == '2':
            self.tables = normalizeTo2NF(self)
        elif normal_form == '3':
            self.tables = normalizeTo3NF(self)
        elif normal_form == 'B':
            self.tables = normalizeToBCNF(self)
        #elif normal_form == '4':
        #    self.tables = normalizeTo4NF(self)
        #elif normal_form == '5':
        #    self.tables = normalizeTo5NF(self)
    
    """ Finds the highest specified normal form of the input table using Table
        methods on self.original_table
        Input: self
        Output: None
    """
    def findHighestNF(self) -> None:
        print("Highest normal form of the input table: ", end="")
        #if self.original_table.is5NF():
            #print("5NF")
        #elif self.original_table.is4NF():
            #print("4NF")
        if self.original_table.isBCNF():
            print("BCNF")
        elif self.original_table.is3NF():
            print("3NF")
        elif self.original_table.is2NF():
            print("2NF")
        elif self.original_table.is1NF():
            print("1NF")
        else:
            print("None. Input table does not satisfy any normal form.")
        
""" Functions to normalize all tables in DB schema
    Input: the DB schema
    Output: list of normalized tables
"""
def normalizeTo1NF(databaseSchema: DatabaseSchema) -> list[T.Table]:
    normalizedDatabaseSchema: list[T.Table] = []
    normalized_tables: set[T.Table]

    for table in databaseSchema.tables: # normalize each table in schema to 1NF
        normalized_tables = T.normalizeTo1NF(table) 
        for n_table in normalized_tables: # store each newly normalized table
            normalizedDatabaseSchema.append(n_table)

    return normalizedDatabaseSchema

def normalizeTo2NF(databaseSchema: DatabaseSchema) -> list[T.Table]:
    normalizedDatabaseSchema: list[T.Table] = normalizeTo1NF(databaseSchema)
    normalized_tables: set[T.Table]

    for table in databaseSchema.tables: # normalize each table in schema to 2NF
        normalized_tables = T.normalizeTo2NF(table) 
        for n_table in normalized_tables: # store each newly normalized table
            normalizedDatabaseSchema.append(n_table)
    
    return normalizedDatabaseSchema

def normalizeTo3NF(databaseSchema: DatabaseSchema) -> list[T.Table]:
    normalizedDatabaseSchema: list[T.Table] = normalizeTo2NF(databaseSchema)
    normalized_tables: set[T.Table]

    for table in databaseSchema.tables: # normalize each table in schema to 3NF
        normalized_tables = T.normalizeTo3NF(table) 
        for n_table in normalized_tables: # store each newly normalized table
            normalizedDatabaseSchema.append(n_table)
    
    return normalizedDatabaseSchema

def normalizeToBCNF(databaseSchema: DatabaseSchema) -> list[T.Table]:
    normalizedDatabaseSchema: list[T.Table] = normalizeTo3NF(databaseSchema)
    normalized_tables: set[T.Table]

    for table in databaseSchema.tables: # normalize each table in schema to BCNF
        normalized_tables = T.normalizeToBCNF(table) 
        for n_table in normalized_tables: # store each newly normalized table
            normalizedDatabaseSchema.append(n_table)
    
    return normalizedDatabaseSchema
""" Add back in when 4NF and 5NF functions are made
def normalizeTo4NF(databaseSchema: DatabaseSchema) -> list[T.Table]:
    normalizedDatabaseSchema: list[T.Table] = normalizeToBCNF(databaseSchema)
    normalized_tables: set[T.Table]

    for table in databaseSchema.tables: # normalize each table in schema to 4NF
        normalized_tables = T.normalizeTo4NF(table) 
        for n_table in normalized_tables: # store each newly normalized table
            normalizedDatabaseSchema.append(n_table)
    
    return normalizedDatabaseSchema

def normalizeTo5NF(databaseSchema: DatabaseSchema) -> list[T.Table]:
    normalizedDatabaseSchema: list[T.Table] = normalizeTo4NF(databaseSchema)
    normalized_tables: set[T.Table]

    for table in databaseSchema.tables: # normalize each table in schema to 5NF
        normalized_tables = T.normalizeTo5NF(table) 
        for n_table in normalized_tables: # store each newly normalized table
            normalizedDatabaseSchema.append(n_table)
    
    return normalizedDatabaseSchema
"""