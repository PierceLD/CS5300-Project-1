import Attribute as A
import Row as R

class DataTable():
    attributeSet: set[A.Attribute]
    rowList: list[R.Row]
    
    def __init__(self, attributeSet: set[A.Attribute], rowList: list[R.Row]) -> None:
        self.attributeSet = attributeSet
        self.rowList = rowList
        
    def addRow(self, row: R.Row) -> None:
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
                    if row.rowDictionary[attribute] != joinRow.rowDictionary[attribute]:
                        shouldJoinRows = False
                        
                if shouldJoinRows:
                    newRowDictionary: dict[A.Attribute, str] = {}
                    for attribute in newAttributeSet:
                        if attribute in self.attributeSet:
                            newAttributeSet[attribute] = row.rowDictionary[attribute]
                        else:
                            newAttributeSet[attribute] = joinRow.rowDictionary[attribute]
                    newDataTable.addRow(R.Row(newAttributeSet, newRowDictionary))
        return newDataTable
            