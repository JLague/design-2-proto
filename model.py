from numpy import double
import db
from PySide6.QtCore import QAbstractTableModel, Qt


class FactureModel(QAbstractTableModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.facture = []
        self.headers = ['UPC', 'Format', 'Description', 'Prix unitaire', 'Quantité']
        self.db = db.UPCDatabase()
        self.total = 0.0

    def rowCount(self, parent=None):
        return len(self.facture)

    def columnCount(self, parent=None):
        return len(self.headers)

    def data(self, index, role=None):
        if not index.isValid():
            return None
        elif role != Qt.DisplayRole:
            return None
        
        # Format price
        item = self.facture[index.row()][index.column()]
        if index.column() == 3:
            return '{:.2f} $'.format(item)
        return item

    def headerData(self, section, orientation, role=None):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.headers[section]
        return None
    
    def remove_rows(self, indices: list[int]):
        for index in indices:
            self.total -= self.facture[index.row()][3] * self.facture[index.row()][4]
            self.facture.pop(index.row())
        self.layoutChanged.emit()
    
    def add_upc(self, upc: str) -> bool:
        # If upc already in table, update quantity
        for row in self.facture:
            if upc == row[0]:
                self.layoutAboutToBeChanged.emit()
                row[4] += 1
                self.total += row[3]
                self.layoutChanged.emit()
                return True
        
        # Get UPC info from database
        new_row = self.db.get_upc_info(upc)

        # If UPC not found, return False
        if new_row is None:
            return False
        
        # Add info row to table and update total
        self.layoutAboutToBeChanged.emit()
        new_row = list(new_row)
        new_row.append(1)
        self.facture.append(new_row)
        self.total += double(new_row[3])
        self.layoutChanged.emit()
        return True

    def clear_facture(self):
        self.facture.clear()
        self.total = 0.0
        self.layoutChanged.emit()

    def get_total_str(self) -> str:
        s = str.format('{:.2f} $', self.total)
        return s
