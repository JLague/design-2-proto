import model
import sys
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *

TEST_UPC = "715067004297"


class MainView(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.menu = self.menuBar()
        self.file_menu = self.menu.addMenu('File')

        exit_action = QAction('Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.exit_app)

        self.file_menu.addAction(exit_action)

        self.main_widget = MainWidget()
        self.setCentralWidget(self.main_widget)
    
    @Slot()
    def exit_app(self, checked):
        QApplication.quit()


class MainWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        # Facture table
        self.facture_model = model.FactureModel()
        self.facture_table = QTableView()
        self.facture_table.setModel(self.facture_model)
        self.facture_table.horizontalHeader().setStretchLastSection(True)
        self.facture_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        
        self.facture_model.add_upc(TEST_UPC)

        self.down = QFormLayout()
        self.facture_total = QLabel()
        # self.facture_total.setAlignment(Qt.AlignRight)
        self.down.addRow("Total: ", self.facture_total)
        self.down.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)
        # self.down.setAlignment(Qt.AlignRight)
        self.down.setLabelAlignment(Qt.AlignRight)
        self.update_total()

        self.left = QVBoxLayout()
        self.left.addWidget(self.facture_table)
        self.left.addLayout(self.down)
        # self.left.setAlignment(self.down, Qt.AlignRight)

        self.upc_input = QLineEdit()
        self.upc_input.setPlaceholderText("UPC")
        self.add = QPushButton("Ajouter UPC")
        self.delete_rows = QPushButton("Effacer les lignes")
        self.clear = QPushButton("Vider")

        self.right = QFormLayout()
        self.right.addRow("UPC: ", self.upc_input)
        self.right.addRow(self.add)
        self.right.addRow(self.delete_rows)
        self.right.addRow(self.clear)
        self.right.setFieldGrowthPolicy(QFormLayout.FieldsStayAtSizeHint)

        self.layout = QHBoxLayout()
        self.layout.addLayout(self.left)
        self.layout.setStretchFactor(self.left, 1)
        self.layout.addLayout(self.right)
        self.setLayout(self.layout)
        self.facture_table.resizeColumnsToContents()

        self.set_behavior()
    
    def set_behavior(self):
        self.add.clicked.connect(self.add_upc)
        self.clear.clicked.connect(self.clear_facture)
        self.facture_model.layoutChanged.connect(self.update_total)
        self.delete_rows.clicked.connect(self.remove_upcs)

    def add_upc(self):
        upc = self.upc_input.text()
       
        # Check if upc is valid
        if len(upc) != 12 or not upc.isdigit() or not self.facture_model.add_upc(upc):
            show_error_dialog("UPC invalide ou non existant")
                 
    def clear_facture(self):
        self.facture_model.clear_facture()
    
    def remove_upcs(self):
        self.facture_model.remove_rows(self.facture_table.selectedIndexes())
        self.facture_table.clearSelection()

    def update_total(self):
        self.facture_total.setText(self.facture_model.get_total_str())

def show_error_dialog(msg: str):
    msg_box = QMessageBox()
    msg_box.setIcon(QMessageBox.Critical)
    msg_box.setText(msg)
    msg_box.setWindowTitle("Erreur")
    msg_box.exec()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainView()
    window.setWindowTitle('Équipe 12 - PIE Engineering')
    window.resize(1000,800)
    window.show()

    sys.exit(app.exec())