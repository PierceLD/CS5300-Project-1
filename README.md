# Database Relation Normalizer
### Developed by: Pierce Dreiling, Adam McNeil, and Daniel Martin  
### Objects and functions:
For our basic structure, we created class objects corresponding to a specific aspect of a database relation including attributes, functional dependencies, tables and the database schema itself.  

**Attribute.py**
- An Attribute object holds an attribute's name, SQL data type, prime status, and multi-valued status.  

**FunctionalDependency.py**
- A FunctionalDependency object holds both the left-hand side (determinant) and the right-hand side (non-determinant or dependent) of a functional dependency, as well as the multi-valued status, which is used to differentiate between regular FDs and multi-valued FDs when normalizing.  

**Table.py**
- A Table object contains it's name, attributes, primary key, and functional dependencies.
- It also has member functions for checking which normal form it is in (*is#NF()*)and also helper functions for getting specific attributes or comparing an inputted set of attributes or functional dependencies to it's own sets.
- The other non-member functions (*normalizeTo#NF()*) in the same file are the normalization functions for 1NF to 5NF, where a table is inputted and a set of tables is outputted representing the original relation altered/decomposed in the respective normal form.  

**DatabaseSchema.py**
- A DatabaseSchema object stores the original input table, un-altered, and a list of Table objects, which holds all of the tables resulting from decomposing the original input table. This is the object created in main.py to start the process of decomposition.
- The general *normalize()* member function is used to normalize the schema, which is basically looping through the list of tables and normalizing each one individually by calling the appropriate normalization function.
- *findHighestNF()* is used to find the highest normal form of the original input table
- *createSQLQueries()* is the SQL query generator which will write out the generated queries to a text file name "SQLQueries.txt"
- The non-member functions in the same file are called by the DatabaseSchema object's members to assist in either normalization or query generation. The *normalizeTo#NF()* functions loop through each table in the schema's list and calls the table's *normalizeTo#NF()* method. *findForeignKeys()* and *createReferenceTable()* are used to determine how to generate foreign key constraints and reference tables for the queries.  

**main.py**
- 

### Input Parser
Our input parser is represented by the file **Parse.py** which will parse and stored all the data from the input csv file and the user-inputted functional dependencies to then create the Table object and its components.
- *csvParse()* will get all the attributes and data from the inputted csv file, and store them into a dictionary of dictionaries, representing the structure of the table data.
- *getDataType()* and *keyParse()* will determine an attribute's data type and which attributes are a part of the table's primary key, which is specified by the user.
- *fdParse()* will take the inputted functional dependencies and create a set of FD objects for the Table  

### Normalizer
The actual normalization functions that decompose/alter a table are in Table.py where each function only takes one table as input.  
The normalization functions in DatabaseSchema.py are meant call a normalization function from Table.py for each table in a DatabaseSchema's tables list.  

### SQL Query Generator
**DatabaseSchema.py** contains the SQL query generator and the DatabaseSchema object created in **main.py** will call its member function, *createSQLQueries()*, to generate the SQL queries.  

### Normal Form Finder
This is also contained in **DatabaseSchema.py** and the DatabaseSchema object in **main.py** will call its respective member function, *findHighestNF()*, to find the highest normal form of the original input table.  

