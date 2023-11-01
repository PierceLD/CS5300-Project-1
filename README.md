# Database Relation Normalizer
### Developed by: Pierce Dreiling, Adam McNeil, and Daniel Martin  
### Notes for correctly entering input:  
The following are necessary for correctly inputting data:
- Run **main.py**
- In the csv file, to indicate a multi-valued attribute in a single cell, wrap the cell data with double-quotes and separate data values with a comma. i.e "X,Y,Z" for a multi-valued attribute Project.
- Indicate the primary key of the relation by typing the attribute names separated by a comma (if composite PK). i.e. StudentID, Course
- Input all necessary, non-trivial functional dependencies (both regular and multi-valued):
    - For regular dependencies use a single arrow. 
        - i.e. `StudentID -> Course`
    - Separate attributes with a comma. 
        - i.e. `StudentID, Course -> FirstName, Instructor`
    - For regular dependencies, do not write separate FDs for dependencies with the same determinant. i.e `StudentID -> FirstName` and `StudentID -> LastName` should be inputted as `StudentID -> FirstName, LastName`
        - i.e. `StudentID -> FirstName, LastName`
    - For multi-valued dependencies use a double arrow. 
        - i.e. `Ename ->-> Dname`
    - If you have a multi-valued dependency that can be written in shorthand as `Ename ->-> Dname | Ename`, please separate it into two separate multi-valued dependencies. 
        - i.e. `Ename ->-> Dname` (enter) `Ename ->-> Pname` (enter)
    - Type "exit" to stop inputting FDs.
- Follow prompt for which normalization you want to reach and type corresponding numbers or letter.
- Indicate whether you want to find the highest normal form of the input table. This will be outputted, if you chose to, in SQLQueries.txt along with the generated CREATE TABLE queries.  

### Output:
- SQL Queries in a text file SQLQueries.txt
    - Highest normal form of the input table is also outputted to that file (if opted)
- Relation table outputted in console in the specified normal form

### Objects and functions:
For our basic structure, we created class objects corresponding to a specific aspect of a database relation including attributes, functional dependencies, tables and the database schema itself.  

**Attribute.py**
- An Attribute object holds an attribute's name, SQL data type, prime status, and multi-valued status.  

**FunctionalDependency.py**
- A FunctionalDependency object holds both the left-hand side (determinant) and the right-hand side (non-determinant or dependent) of a functional dependency, as well as the multi-valued status, which is used to differentiate between regular FDs and multi-valued FDs when normalizing.  

**Table.py**
- A Table object contains it's name, attributes, primary key, and functional dependencies.
- It also has member functions for checking which normal form it is in--`is#NF()`--and also helper functions for getting specific attributes or comparing an inputted set of attributes or functional dependencies to it's own sets.
- The other non-member functions--`normalizeTo#NF()`--in the same file are the normalization functions for 1NF to 5NF, where a table is inputted and a set of tables is outputted representing the inputted table altered/decomposed in the respective normal form.
- `dataProject()` is used to properly project data tuples into each decomposed table of a base relation.  
- For 5NF, we narrowed it down so that a table with 3 prime attributes will only be decomposed (if necessary). A table with more or less prime attributes will be ignored.

**DatabaseSchema.py**
- A DatabaseSchema object stores the original input table, un-altered, and a list of Table objects, which holds all of the tables resulting from decomposing the original input table. This is the object created in **main.py** to start the process of decomposition.
- The general `normalize()` member function is used to normalize the schema, which calls the appropriate normalization function.
- Each `normalizeTo#NF()` function loops through the list of tables and normalizes each table separately by calling each table's normalization function.
- `findHighestNF()` is used to find the highest normal form of the original input table
- `createSQLQueries()` is the SQL query generator which will write out the generated queries to a text file name "SQLQueries.txt"
- The non-member functions in the same file are called by the DatabaseSchema object's members to assist in either normalization or query generation. The `normalizeTo#NF()` functions loop through each table in the schema's list and calls the table's `normalizeTo#NF()` method. `findForeignKeys()` and `createReferenceTable()` are used to determine how to generate foreign key constraints and reference tables for the queries.  

**main.py**
1. For the flow of our main program, the user is first prompted to enter the .csv file containing their relation table they want to normalize and the data values associated with it.
2. The csv file is parsed and a set of Attribute objects is created by calling `csvParse()`.
3. The user is then prompted to enter the primary key of the table, which is used to determine which attributes in the set should have their `isPrime` member variable set to True.
4. The user is prompted to enter the functional dependencies according to the format specified above, and a set of FunctionalDependency objects is created by calling `fdParse()`.
5. The Table object is created with the sets of Attribute and FunctionalDependency objects, and the input table name is the name of the .csv file.
6. The DatabaseSchema object is then created with the newly created Table object passed to it's constructor.
7. The user is then prompted to enter the normal form they want to reach for the input table, and the DatabaseSchema object calls it's `normalize()` method to start normalizing the input relation.
8. The user is then prompted to enter if they want to find the highest normal form of their input table, and if so, the DatabaseSchema object calls it's `findHighestNF()` method.
9. Lastly, the DatabaseSchema object calls its `createSQLQueries()` method to generate the CREATE TABLE queries for the user and the highest normal form of their input table (if opted) and outputs the results to a text file "SQLQueries.txt".

#### **Input Parser**
Our input parser is represented by the file **Parse.py** which will parse and stored all the data from the input csv file and the user-inputted functional dependencies to then create the Table object and its components.
- `csvParse()` will get all the attributes and data from the inputted csv file, and store them into a dictionary of dictionaries, representing the structure of the table data.
- `getDataType()` and `keyParse()` will determine an attribute's data type and which attributes are a part of the table's primary key, which is specified by the user.
- `fdParse()` will take the inputted functional dependencies and create a set of FD objects for the Table.  

#### **Normalizer**
The actual normalization functions that decompose/alter a table are in Table.py where each function only takes one table as input.  
The normalization functions in DatabaseSchema.py are meant to call a normalization function from Table.py for each table in a DatabaseSchema's tables list.
For 5NF, we are assuming that any table with less than 3 attributes or greater than 3 attributes is already in 5NF, for simplicity.

#### **SQL Query Generator**
**DatabaseSchema.py** contains the SQL query generator and the DatabaseSchema object created in **main.py** will call its member function, `createSQLQueries()`, to generate the SQL queries.  

#### **Normal Form Finder**
This is also contained in **DatabaseSchema.py** and the DatabaseSchema object in **main.py** will call its respective member function, `findHighestNF()`, to find the highest normal form of the original input table.  

