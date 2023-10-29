import Attribute as A
import DataTable as DT

class Row():
    dataTable: DT.DataTable
    rowDictionary: dict[A.Attribute, str]
    
    def __init__(self, dataTable: DT.DataTable, rowDictionary: dict[A.Attribute, str]) -> None:
        self.dataTable = dataTable
        self.rowDictionary = rowDictionary
    
    def project(self, projectSet: set[A.Attribute], newDataTable: DT.DataTable) -> 'Row':
        newRowDictionary: dict[A.Attribute, str] = {}
        for attribute in projectSet:
            newRowDictionary[attribute] = self.rowDictionary[attribute]
        return Row(projectSet, newDataTable)
            