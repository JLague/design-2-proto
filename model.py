import db
from PySide6.QtCore import QAbstractTableModel, Qt


class FactureModel(QAbstractTableModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.facture = []
        self.headers = ['UPC', 'Format', 'Description', 'Prix']
        self.db = db.UPCDatabase()

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
        row = self.db.get_upc_info(upc)
        if row is None:
            return False
        self.facture.append(row)
        self.layoutChanged.emit()
        return True

    def clear_facture(self):
        self.facture.clear()
        self.layoutChanged.emit()
    
