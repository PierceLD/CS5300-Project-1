import Attribute as A

class DataTable():
    attributeSet: set[A.Attribute]
    rowList: list['Row']
    
    def __init__(self, attributeSet: set[A.Attribute], rowList: list['Row']) -> None:
        self.attributeSet = attributeSet
        self.rowList = rowList
        
    def __str__(self) -> str:
        returnStr: str = ""
        for attribute in self.attributeSet:
            returnStr += attribute.name + ", "
        returnStr += "\n"
        for row in self.rowList:
            returnStr += row.__str__() + "\n"
        return returnStr
        
    def addRow(self, row: 'Row') -> None:
        self.rowList.append(row)    
    
    def project(self, projectSet: set[A.Attribute]) -> 'DataTable':
        newDataTable: DataTable = DataTable(projectSet, [])
        for row in self.rowList:
            newDataTable.addRow(row.project(projectSet=projectSet, newDataTable=newDataTable))
        return newDataTable
    
    def equalJoin(self, joinAttributes: set[A.Attribute], joinTable: 'DataTable') -> 'DataTable':
        newAttributeSet: set[A.Attribute] = self.attributeSet.union(joinTable.attributeSet)
        newDataTable: DataTable = DataTable(newAttributeSet, [])
        
        for row in self.rowList:
            for joinRow in joinTable.rowList:
                shouldJoinRows: bool = True
                for attribute in joinAttributes:
                    if not row.rowDictionary[attribute] == joinRow.rowDictionary[attribute]:
                        shouldJoinRows = False
                        
                if shouldJoinRows:
                    newRowDictionary: dict[A.Attribute, str] = {}
                    for attribute in newAttributeSet:
                        if attribute in self.attributeSet:
                            newRowDictionary[attribute] = row.rowDictionary[attribute]
                        else:
                            newRowDictionary[attribute] = joinRow.rowDictionary[attribute]
                    newDataTable.addRow(Row(newAttributeSet, newRowDictionary))
        return newDataTable
    
    def equal(self, otherTable: 'DataTable') -> bool:
        if len(self.attributeSet) != len(self.attributeSet.union(otherTable.attributeSet)):
            return False
        if len(self.rowList) != len(otherTable.rowList):
            return False
        for row in self.rowList:
            if not otherTable.contains(row):
                return False
        return True
    
    def contains(self, testRow: 'Row') -> bool:
        for row in self.rowList:
            if testRow.equal(row):
                return True
        return False
    
def reduce(dataTable: DataTable) -> DataTable:
    newDataTable: DataTable = DataTable(dataTable.attributeSet, [])
    for row in dataTable.rowList:
        if not newDataTable.contains(row):
            newDataTable.addRow(row)   
    return newDataTable

class Row():
    dataTable: DataTable
    rowDictionary: dict[A.Attribute, str]
    
    def __init__(self, dataTable: DataTable, rowDictionary: dict[A.Attribute, str]) -> None:
        self.dataTable = dataTable
        self.rowDictionary = rowDictionary
    
    def project(self, projectSet: set[A.Attribute], newDataTable: DataTable) -> 'Row':
        newRowDictionary: dict[A.Attribute, str] = {}
        for attribute in projectSet:
            newRowDictionary[attribute] = self.rowDictionary[attribute]
        return Row(newDataTable, newRowDictionary)
    
    def __str__(self) -> str:
        returnStr: str = ""
        for key in self.rowDictionary:
            returnStr += self.rowDictionary[key] + ", "
        return returnStr
    
    def equal(self, otherRow: 'Row') -> bool:
        if len(self.rowDictionary) != len(otherRow.rowDictionary):
            return False
        for key in self.rowDictionary:
            if self.rowDictionary[key] != otherRow.rowDictionary[key]:
                return False
        return True