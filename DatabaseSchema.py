# basically just a list of tables (needs to be changed to tables)
import Table as T
import Attribute as A
import FunctionalDependency as FD
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

    """ Creates the SQL Queries and outputs them to SQLQueries.txt
    """
    def createSQLQueries(self) -> None:
        with open("SQLQueries.txt", "w") as f:
            for table in self.tables:
                print(f"CREATE TABLE {table.name} (", file=f)
                for attr in table.attributes:
                    if attr.dataType == "VARCHAR":
                        s: str = f"\t{attr.name} {attr.dataType}(100)"
                    else:
                        s = f"\t{attr.name} {attr.dataType}"
                    if attr.isPrime:
                        s += " PRIMARY KEY,"
                    else:
                        s += ","
                    print(s, file=f)
                # determine foreign key attributes, create a new function
                fk_queries: list[str] = findForeignKeys(self, table)
                for i in range(len(fk_queries)):
                    if i == len(fk_queries)-1: # if last query
                        print(fk_queries[i], file=f)
                    else:
                        print(fk_queries[i] + ",", file=f)
                print(");", file=f)
            # create many-to-many relation table if original primary key is composite
            print(createReferenceTable(self), file=f)
            print(self.findHighestNF(), file=f)
                
        return

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
""" Creates foreign key constraints for inputted table, if any exist
    Input: DatabaseSchema, table
    Output: list of SQL queries to create foreign key constraints for input table
"""
def findForeignKeys(databaseSchema: DatabaseSchema, table: T.Table) -> list[str]:
    queries: list[str] = []
    fk_query: str = ""

    for t in databaseSchema.tables:
        if t.name != table.name: # skip over same table
            for attr1 in table.attributes:
                if not attr1.isPrime(): # if attribute is non-prime
                    for attr2 in t.attributes:
                        if attr2.isPrime and (attr1.name == attr2.name): # if attribute is a primary key in another table
                            fk_query = f"FOREIGN KEY ({attr1.name}) REFERENCES {t.name}s({attr2.name})"
                            queries.append(fk_query)

    return queries

def createReferenceTable(databaseSchema: DatabaseSchema) -> list[str]:
    original_PK: set[tuple[str, str]] = set([(attr.name, attr.dataType) for attr in databaseSchema.original_table.primaryKey])
    table_query: str = ""
    ref_table_name: str = ""
    ref_table_attributes: list[tuple[str, str]] = []
    if len(original_PK) > 1: # composite key indicates many to many relationship

        # first find the tables to reference
        disconnected_tables: list[T.Table] = []
        for table in databaseSchema.tables:
            table_PK: set[str] = set([key.name for key in table.primaryKey])
            if table_PK < original_PK: # if current table's PK is a proper subset of original PK (means original relation was split)
                disconnected_tables.append(table)

        # create reference relation for the disconnected tables
        table_query += "CREATE TABLE "
        for table in disconnected_tables:
            ref_table_name += table.name
        table_query += f"{ref_table_name}s (\n"

        # find attributes for reference relation
        for table in disconnected_tables:
            for key in table.primaryKey:
                ref_table_attributes.append((key.name, key.dataType))

        # create SQL attribute declarations
        for attr in ref_table_attributes:
            if key.dataType == "VARCHAR":
                table_query += f"\t{attr.name} {attr.dataType}(100),\n"
            else:
                table_query += f"\t{attr.name} {attr.dataType},\n"

        # create foreign key constraints
        for table, i in enumerate(disconnected_tables):
            for key, j in enumerate(table.primaryKey):
                if (i == len(disconnected_tables)-1) and (j == len(disconnected_tables)-1): # if very last SQL statement
                    table_query += f"FOREIGN KEY ({key.name}) REFERENCES {table.name}s({key.name})\n"
                else:
                    table_query += f"FOREIGN KEY ({key.name}) REFERENCES {table.name}s({key.name}),\n"

        table_query += ");\n"

    return table_query