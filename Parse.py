import csv
import re
import Attribute as A
import FunctionalDependency as FD

""" Parses the relation in the .csv file to get attributes
    Input: .csv file
    Output: list of Attribute objects
"""
def csvParse(filename: str) -> set[A.Attribute]:
    attributes: set[A.Attribute] = set()

    with open(filename, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        headings: list[str] = next(csv_reader) # gets first line of file (attributes)
        tuple1: list[str] = next(csv_reader) # gets first line of data
        # determines SQL data type for each attribute based on data vals in first tuple of the table
        for i, val in enumerate(tuple1):
            val = val.split(',') # splits data string into a list to check for multiple values
            if len(val) > 1: # if attribute is multi valued
                multVals: bool = True
            else:
                multVals = False
            d_type: str = getDataType(val[0])
            attributes.add(A.Attribute(name=headings[i], isMultiValued=multVals, dataType=d_type))

        csv_file.close()

    return attributes

""" Takes a string representing a data value from the table to
    determine SQL data type for the corresponding attribute using regex
    Input: list of data values represented as strings
    Output: string indicating SQL data type
"""
def getDataType(data_val: str) -> str:
    is_date = re.search("^([1-9]|(1[0-2]))/([1-9]|(1[0-9])|(2[0-9])|(3[0-1]))/[0-9]{4}$", data_val)
    is_integer = re.search("^-?[0-9]+$", data_val)
    
    if is_date:
        return "DATE"
    elif is_integer:
        return "INT"
    
    return "VARCHAR" # if not a date or a number or can't determine it, then just assume a string

""" Takes inputted key, parses it into a set
    Input: string indication primary key of inputted table
    Output: set of strings indicating prime attributes
"""
def keyParse(key: str) -> set[str]:
    key_set: set[str] = set()

    parsed_key: list[str] = [x.strip() for x in key.split(',')]
    
    for k in parsed_key:
        key_set.add(k)

    return key_set


""" Parse each inputted functional dependency (strings) into FD objects
    Input: list of inputted strings representing FDs
    Output: list of FD objects representing each specified FD for input relation
"""
def fdParse(fd_list: list[str], primary_key: set[str], attributes: set[A.Attribute]) -> list[FD.FunctionalDependency]:
    partitioned_fd: tuple[str, str, str] = tuple()
    lhs: list[str] = [] # left side of fd
    rhs: list[str] = [] # right side of fd
    determinants: set[A.Attribute] = set()
    non_determinants: set[A.Attribute] = set()
    parsed_fds: list[FD.FunctionalDependency] = []
    isMultiValued: bool

    # for each user-inputted functional dependency string
    for fd in fd_list: 
        if "->->" in fd: # for multi-valued dependencies
            partitioned_fd = fd.partition("->->")
            isMultiValued = True
        elif "->" in fd: # for regular dependencies
            partitioned_fd = fd.partition("->")
            isMultiValued = False
        
        # each attribute split into list element e.g. ["CourseStart", "CourseEnd"]
        lhs = [x.strip() for x in partitioned_fd[0].split(',')] 
        rhs = [x.strip() for x in partitioned_fd[2].split(',')]
        
        # making each attribute string into Attribute object, add to corresponding set
        isPrime: bool = False
        # creating determinants list of Attribute objects
        for attr in lhs: 
            """if attr in primary_key: # if the current attribute is part of primary key
                isPrime = True
            else:
                isPrime = False"""
            for attribute in attributes:
                if attr == attribute.name:
                    determinants.add(attribute) 
        # creating non-determinants list of Attribute objects
        for attr in rhs: 
            """if attr in primary_key:
                isPrime = True
            else:
                isPrime = False"""
            for attribute in attributes:
                if attr == attribute.name:
                    non_determinants.add(attribute)  
        
        # creating FunctionDependency object with determinants and non_determinants, add to list
        parsed_fds.append(FD.FunctionalDependency(determinants, non_determinants, isMultiValued))
        
        # clear sets for next loop
        determinants = set()
        non_determinants = set()
    
    # make attributes in each FD have the correct data types, TODO: not necesssary now that any attribute in an FD references an attribute in attributes list
    """for fd in parsed_fds:
        for determinant in fd.determinants:
            for attr in attributes:
                if determinant.name == attr.name:
                    determinant = attr
        for non_determinant in fd.nonDeterminants:
            for attr in attributes:
                if non_determinant.name == attr.name:
                    determinant = attr"""
    
    return parsed_fds
