import csv
import Table as T
import Attribute as A
import FunctionalDependency as FD

""" Parses the relation in the .csv file to get attributes
    Input: .csv file
    Output: list of Attribute objects
"""
def csvParse(filename: str) -> list[A.Attribute]:
    attributes: list[A.Attribute] = []

    with open(filename, 'r') as csv_file:
        reader = csv.reader(csv_file)
        for attribute in reader[0]: # getting each column attribute from first row of .csv file
            attributes.append(attribute)
        csv_file.close()

    return attributes

""" Takes inputted key, parses it into a set
    Input: string indication primary key of inputted table
    Output: set of strings indicating prime attributes
"""
def keyParse(key: str) -> set[str]:
    key_set: set[str] = set()
    parsed_key = [x.strip() for x in key.split(',')]
    for k in parsed_key:
        key_set.add(k)
    return key_set


""" Parse each inputted functional dependency (strings) into FD objects
    Input: list of inputted strings representing FDs
    Output: list of FD objects representing each specified FD for input relation
"""
def fdParse(fd_list: list[str], primary_key: set[str]) -> list[FD.FunctionalDependency]:
    partitioned_fd: tuple[str, str, str] = tuple()
    lhs: list[str] = [] # left side of fd
    rhs: list[str] = [] # right side of fd
    determinants: set[A.Attribute] = set()
    non_determinants: set[A.Attribute] = set()
    parsed_fds: list[FD.FunctionalDependency] = []

    # for each user-inputted functional dependency string
    for fd in fd_list: 
        if "->->" in fd: # for multi-valued dependencies
            partitioned_fd = fd.partition("->->")
        elif "->" in fd: # for regular dependencies
            partitioned_fd = fd.partition("->")
        
        # each attribute split into list element e.g. ["CourseStart", "CourseEnd"]
        lhs = [x.strip() for x in partitioned_fd[0].split(',')] 
        rhs = [x.strip() for x in partitioned_fd[2].split(',')]
        
        # making each attribute string into Attribute object, add to corresponding set
        isPrime: bool = False
        # creating determinants list of Attribute objects
        for attr in lhs: 
            if attr in primary_key: # if the current attribute is part of primary key
                isPrime = True
            else:
                isPrime = False
            determinants.add(A.Attribute(attr, isPrime)) 
        # creating non-determinants list of Attribute objects
        for attr in rhs: 
            if attr in primary_key:
                isPrime = True
            else:
                isPrime = False
            non_determinants.add(A.Attribute(attr, isPrime)) 
        
        # creating FunctionDependency object with determinants and non_determinants, add to list
        parsed_fds.append(FD.FunctionalDependency(determinants, non_determinants))

    return parsed_fds
