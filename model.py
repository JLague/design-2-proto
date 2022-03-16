from numpy import double
import db
from PySide6.QtCore import QAbstractTableModel, Qt


class FactureModel(QAbstractTableModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.facture = []
        self.headers = ['UPC', 'Format', 'Description', 'Prix', 'Quantité']
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
        return self.facture[index.row()][index.column()]

    def headerData(self, section, orientation, role=None):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.headers[section]
        return None
    
    def add_upc(self, upc: str) -> bool:
        for row in self.facture:
            if upc == row[0]:
                row[4] += 1
                self.dataChanged.emit()
                return True
        
        new_row = self.db.get_upc_info(upc)
        if new_row is None:
            return False
        self.facture.append(new_row)
        self.facture.append(new_row + [1])
        self.layoutChanged.emit()
        self.total += double(row[3])
        return True

    def clear_facture(self):
        self.facture.clear()
        self.total = 0.0
        self.layoutChanged.emit()

    def get_total(self):
        return str(self.total)
