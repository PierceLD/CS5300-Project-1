# basically just a list of tables (needs to be changed to tables)
import Table as T
from copy import deepcopy

class DatabaseSchema:
    original_table: T.Table
    tables: list[T.Table]
    
    def __init__(self, original_table: T.Table, tables: list[T.Table] = []) -> None:
        self.original_table = deepcopy(original_table)
        self.tables = tables
        self.tables.append(self.original_table) # add og input table to list of tables

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

    """ Pretty print all tables
        Input: self
        Output: str
    """
    def __str__(self) -> str:
        output: str = ""

        for table in self.tables:
            output += '-'*20
            output += "\nAttributes: "
            for attr in table.attributes:
                output += attr.name + ", "
            output += "\nPrimary Key: { "
            for attr in table.attributes:
                if attr.isPrime:
                    output += attr.name + ", "
            output += "}\n"
            output += "\nFunctional Dependencies: \n"
            for fd in table.functionalDependencies:
                output += "\t{ "
                for attr in fd.determinants:
                    output += attr.name + ", "
                output += "} -> { "
                for attr in fd.nonDeterminants:
                    output += attr.name + ", "
                output += "}\n\n"

        return output
        
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
    normalizedDatabaseSchema: list[T.Table] = []
    normalized_tables: set[T.Table]

    databaseSchema.tables = normalizeTo1NF(databaseSchema)

    for table in databaseSchema.tables: # normalize each table in schema to 2NF
        normalized_tables = T.normalizeTo2NF(table) 
        for n_table in normalized_tables: # store each newly normalized table
            normalizedDatabaseSchema.append(n_table)
    
    return normalizedDatabaseSchema

def normalizeTo3NF(databaseSchema: DatabaseSchema) -> list[T.Table]:
    normalizedDatabaseSchema: list[T.Table] = []
    normalized_tables: set[T.Table]

    databaseSchema.tables = normalizeTo2NF(databaseSchema)

    for table in databaseSchema.tables: # normalize each table in schema to 3NF
        normalized_tables = T.normalizeTo3NF(table) 
        for n_table in normalized_tables: # store each newly normalized table
            normalizedDatabaseSchema.append(n_table)
    
    return normalizedDatabaseSchema

def normalizeToBCNF(databaseSchema: DatabaseSchema) -> list[T.Table]:
    normalizedDatabaseSchema: list[T.Table] = []
    normalized_tables: set[T.Table]

    databaseSchema.tables = normalizeTo3NF(databaseSchema)

    for table in databaseSchema.tables: # normalize each table in schema to BCNF
        normalized_tables = T.normalizeToBCNF(table) 
        for n_table in normalized_tables: # store each newly normalized table
            normalizedDatabaseSchema.append(n_table)
    
    return normalizedDatabaseSchema
""" Add back in when 4NF and 5NF functions are made
def normalizeTo4NF(databaseSchema: DatabaseSchema) -> list[T.Table]:
    normalizedDatabaseSchema: list[T.Table] = []
    normalized_tables: set[T.Table]

    databaseSchema.tables = normalizeToBCNF(databaseSchema)

    for table in databaseSchema.tables: # normalize each table in schema to 4NF
        normalized_tables = T.normalizeTo4NF(table) 
        for n_table in normalized_tables: # store each newly normalized table
            normalizedDatabaseSchema.append(n_table)
    
    return normalizedDatabaseSchema

def normalizeTo5NF(databaseSchema: DatabaseSchema) -> list[T.Table]:
    normalizedDatabaseSchema: list[T.Table] = []
    normalized_tables: set[T.Table]

    databaseSchema.tables = normalizeTo4NF(databaseSchema)

    for table in databaseSchema.tables: # normalize each table in schema to 5NF
        normalized_tables = T.normalizeTo5NF(table) 
        for n_table in normalized_tables: # store each newly normalized table
            normalizedDatabaseSchema.append(n_table)
    
    return normalizedDatabaseSchema
"""

def createSQLQueries(databaseSchema: DatabaseSchema):
    
    for table in databaseSchema.tables:
        pass

    return