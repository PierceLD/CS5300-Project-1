# basically just a list of tables (needs to be changed to tables)
import Table as T
import Attribute as A
import FunctionalDependency as FD
from copy import deepcopy

from enum import Enum

class NormalForm(Enum):
    oneNF = [T.normalizeTo1NF]
    twoNF = [T.normalizeTo2NF]
    threeNF = [T.normalizeTo3NF]
    bcNF = [T.normalizeToBCNF]
    fourNF = [T.normalizeTo4NF]
    fiveNF = [T.normalizeTo5NF]
    
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
        elif normal_form == '4':
            self.tables = normalizeTo4NF(self)
        elif normal_form == '5':
            self.tables = normalizeTo5NF(self)
    
    """ Finds the highest specified normal form of the input table using Table
        methods on self.original_table
        Input: self
        Output: output string
    """
    def findHighestNF(self) -> str:
        output: str = "Highest normal form of the input table: "

        if self.original_table.is5NF():
            output += "5NF"
        elif self.original_table.is4NF():
            output += "4NF"
        elif self.original_table.isBCNF():
            output += "BCNF"
        elif self.original_table.is3NF():
            output += "3NF"
        elif self.original_table.is2NF():
            output += "2NF"
        elif self.original_table.is1NF():
            output += "1NF"
        else:
            output += "None. Input table does not satisfy any normal form."
        
        return output

    """ Creates the SQL Queries and outputs them to SQLQueries.txt
    """
    def createSQLQueries(self, find_hnf: str) -> None:
        with open("SQLQueries.txt", "w") as f:
            for table in self.tables:
                print(f"CREATE TABLE {table.name} (", file=f)
                for i, attr in enumerate(table.attributes):
                    if attr.dataType == "VARCHAR":
                        s: str = f"\t{attr.name} {attr.dataType}(100)"
                    else:
                        s = f"\t{attr.name} {attr.dataType}"
                    if attr.isPrime:
                        if i == len(table.attributes) - 1: # if last attribute to print
                            s += " PRIMARY KEY"
                        else:
                            s += " PRIMARY KEY,"
                    else:
                        if i != len(table.attributes) - 1: # if not last attribute to print
                            s += ","
                    print(s, file=f)
                # determine foreign key attributes, create a new function
                fk_queries: list[str] = findForeignKeys(self, table)
                for i in range(len(fk_queries)):
                    if i == len(fk_queries)-1: # if last query
                        print(fk_queries[i], file=f)
                    else:
                        print(fk_queries[i] + ",", file=f)
                print(");\n", file=f)
            # create many-to-many relation table if original primary key is composite
            print(createReferenceTable(self), file=f)
            if find_hnf == "1":
                print(self.findHighestNF(), file=f)
                
        return

    """ Pretty print all tables
        Input: self
        Output: str
    """
    def __str__(self) -> str:
        output: str = ""

        for table in self.tables:
            output += f"\n{table.name}\n"
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

def normalize(databaseSchema: DatabaseSchema, normalForm: NormalForm) -> DatabaseSchema:
    normalizedDatabaseSchema: list[T.Table] = []
    normalized_tables: set[T.Table]

    databaseSchema.tables = normalizeTo4NF(databaseSchema)

    for table in databaseSchema.tables: # normalize each table in schema to 5NF
        normalized_tables = T.normalizeTo5NF(table) 
        for n_table in normalized_tables: # store each newly normalized table
            normalizedDatabaseSchema.append(n_table)
    
    return normalizedDatabaseSchema

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
                if not attr1.isPrime: # if attribute is non-prime
                    for attr2 in t.attributes:
                        if attr2.isPrime and (attr1.name == attr2.name): # if attribute is a primary key in another table
                            fk_query = f"\tFOREIGN KEY ({attr1.name}) REFERENCES {t.name}({attr2.name})"
                            queries.append(fk_query)

    return queries

""" This function creates a reference table for a many-to-many
    relationship, which is determined by the primary key of the
    original relation being composite.
    Input: Database schema object
    Output: String with SQL query to create a reference table, if any
"""
def createReferenceTable(databaseSchema: DatabaseSchema) -> list[str]:
    original_PK: set[str] = set([attr.name for attr in databaseSchema.original_table.primaryKey])
    table_query: str = ""
    ref_table_name: str = ""
    ref_table_attributes: list[tuple[str, str]] = []
    # pre check if there were no partial dependencies to begin with, then new table won't be made for a key in original PK
    

    if (len(original_PK) > 1) and (len(databaseSchema.tables) > 1): # composite key indicates many to many relationship, if decomposed to 2NF

        # first find the tables to reference
        disconnected_tables: list[T.Table] = []
        for table in databaseSchema.tables:
            table_PK: set[str] = set([key.name for key in table.primaryKey])
            tableHasMVFDs: bool = False
            for fd in table.functionalDependencies:
                if fd.isMultiValued:
                    tableHasMVFDs = True
            # TODO: REVISE, I DON'T THINK THIS IS GOOD ENOUGH
            if (table_PK < original_PK) and (not tableHasMVFDs): # if current table's PK is a proper subset of original PK (means original relation was split)
                disconnected_tables.append(table)

        if len(disconnected_tables) > 1: # skip creating the reference table if there are less than 2 disconnected tables
            # create reference relation for the disconnected tables
            table_query += "CREATE TABLE "
            for table in disconnected_tables:
                ref_table_name += table.name
            table_query += f"{ref_table_name} (\n"

            # find attributes for reference relation
            for table in disconnected_tables:
                for key in table.primaryKey:
                    ref_table_attributes.append((key.name, key.dataType))

            # create SQL attribute declarations
            for attr in ref_table_attributes:
                if key.dataType == "VARCHAR":
                    table_query += f"\t{attr[0]} {attr[1]}(100),\n"
                else:
                    table_query += f"\t{attr[0]} {attr[1]},\n"

            # create foreign key constraints
            for i, table in enumerate(disconnected_tables):
                for j, key in enumerate(table.primaryKey):
                    if (i == len(disconnected_tables)-1) and (j == len(table.primaryKey)-1): # if very last SQL statement
                        table_query += f"\tFOREIGN KEY ({key.name}) REFERENCES {table.name}({key.name})\n"
                    else:
                        table_query += f"\tFOREIGN KEY ({key.name}) REFERENCES {table.name}({key.name}),\n"

            table_query += ");\n"

    return table_query