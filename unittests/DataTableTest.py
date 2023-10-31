import unittest
import Attribute as A
import DataTable as DT
import Table as T

class DataTableTest(unittest.TestCase):
    # Define attributes for name, ID, and class
    name_attr = A.Attribute("Name")
    id_attr = A.Attribute("ID")
    class_attr = A.Attribute("Class")
    attributes: set[A.Attribute] = set([name_attr, id_attr, class_attr])


    name_id_table: DT.DataTable = DT.DataTable(set([name_attr, id_attr]), [])
    id_class_table: DT.DataTable = DT.DataTable(set([class_attr, id_attr]), [])

    # Create ten Row objects with name and ID attributes
    row1 = DT.Row(name_id_table, {name_attr: "John", id_attr: "001"})
    row2 = DT.Row(name_id_table, {name_attr: "Alice", id_attr: "002"})
    row3 = DT.Row(name_id_table, {name_attr: "Bob", id_attr: "003"})
    row4 = DT.Row(name_id_table, {name_attr: "Eva", id_attr: "004"})
    row5 = DT.Row(name_id_table, {name_attr: "Mike", id_attr: "005"})
    row6 = DT.Row(name_id_table, {name_attr: "Sara", id_attr: "006"})
    row7 = DT.Row(name_id_table, {name_attr: "Tom", id_attr: "007"})
    row8 = DT.Row(name_id_table, {name_attr: "Linda", id_attr: "008"})
    row9 = DT.Row(name_id_table, {name_attr: "Chris", id_attr: "009"})
    row10 = DT.Row(name_id_table, {name_attr: "Grace", id_attr: "010"})
    table1 = [row1, row2, row3, row4, row5, row6, row7, row8, row9, row10]
    for row in table1:
        name_id_table.addRow(row)

    # Create ten Row objects with ID and class attributes
    row11 = DT.Row(id_class_table, {id_attr: "001", class_attr: "Math"})
    row12 = DT.Row(id_class_table, {id_attr: "002", class_attr: "History"})
    row13 = DT.Row(id_class_table, {id_attr: "003", class_attr: "Science"})
    row14 = DT.Row(id_class_table, {id_attr: "004", class_attr: "Art"})
    row15 = DT.Row(id_class_table, {id_attr: "005", class_attr: "English"})
    row16 = DT.Row(id_class_table, {id_attr: "006", class_attr: "Music"})
    row17 = DT.Row(id_class_table, {id_attr: "007", class_attr: "Physical Education"})
    row18 = DT.Row(id_class_table, {id_attr: "008", class_attr: "Geography"})
    row19 = DT.Row(id_class_table, {id_attr: "009", class_attr: "Computer Science"})
    row20 = DT.Row(id_class_table, {id_attr: "010", class_attr: "Foreign Language"})
    # row21 = DT.Row(id_class_table, {id_attr: "001", class_attr: "History"})
    table2 = [row11, row12, row13, row14, row15, row16, row17, row18, row19, row20]
    for row in table2:
        id_class_table.addRow(row)
        
    joinedTable: DT.DataTable = name_id_table.equalJoin(name_id_table.attributeSet.intersection(id_class_table.attributeSet), id_class_table)
    
    
    
    def testProject(self) -> None:
        print(self.name_id_table)
        print(self.id_class_table)
        print(self.joinedTable)
        print(self.joinedTable.project(set([self.name_attr])))
        
    def test5NF(self) -> None: # this should be in the TableTest.py file but it is a lot easier to have it here and it does not really matter
        table: T.Table = T.Table(attributes=self.attributes, functionalDependencies=set(), name="test table")
        table.dataTable = self.joinedTable
        print(table.is5NF())