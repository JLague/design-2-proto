import db
from PySide6.QtCore import QAbstractTableModel, Qt


class FactureModel(QAbstractTableModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.facture = []
        self.keys = ['upc', 'format', 'desc', 'quantite', 'prix', 'prix_total']
        self.headers = ['UPC', 'Format', 'Description', 'Quantité', 'Prix unitaire', 'Prix total']
        self.db = db.UPCDatabase()

    def rowCount(self, parent=None):
        return len(self.facture)

    def columnCount(self, parent=None):
        return len(self.keys)

    def data(self, index, role=None):
        if not index.isValid():
            return None
        if role == Qt.TextAlignmentRole:
            if self.keys[index.column()] in ['quantite', 'prix', 'prix_total']:
                return int(Qt.AlignRight | Qt.AlignVCenter)
            return Qt.AlignCenter
        elif role != Qt.DisplayRole:
            return None
        
        # Format price
        key = self.keys[index.column()]
        item = self.facture[index.row()][key]
        if 'prix' in key:
            return format_currency(item)
        return item

    def headerData(self, section, orientation, role=None):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.headers[section]
        return None
    
    def remove_rows(self, indices: list[int]):
        for index in indices:
            self.facture.pop(index.row())
        self.layoutChanged.emit()
    
    def add_upc(self, upc: str) -> bool:
        # If upc already in table, update quantity
        for row in self.facture:
            if row['upc'] == upc:
                row['quantite'] += 1
                row['prix_total'] += row['prix']
                self.layoutChanged.emit()
                return True
        
        # Get UPC info from database
        new_row = self.db.get_upc_info(upc)

        # If UPC not found, return False
        if new_row is None:
            return False
        
        # Add info row to table and update total
        self.layoutAboutToBeChanged.emit()
        new_row = dict(new_row)
        new_row['quantite'] = 1
        new_row['prix_total'] = new_row['prix']
        self.facture.append(new_row)
        self.layoutChanged.emit()
        return True

    def clear_facture(self):
        self.facture.clear()
        self.layoutChanged.emit()
    def delete_last_row(self):
        self.facture.pop()
        self.layoutChanged.emit()
        
    def get_total_str(self) -> str:
        total = sum(row['prix_total'] for row in self.facture)
        return format_currency(total)


def format_currency(value: float) -> str:
    return str.format('{:.2f} $', value).replace('.', ',') 
