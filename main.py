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

        facture_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        facture_policy.setHorizontalStretch(1)

        # Facture table
        self.facture_model = model.FactureModel()
        self.facture_table = QTableView()
        self.facture_table.setModel(self.facture_model)
        self.facture_table.horizontalHeader().setStretchLastSection(True)
        self.facture_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.facture_table.setSizePolicy(facture_policy)
        
        self.facture_model.add_upc(TEST_UPC)

        self.down = QFormLayout()
        self.facture_total = QLabel(self.facture_model.get_total()+"  $")
        self.down.addRow("Total: ", self.facture_total)
       

        self.left = QVBoxLayout()
        self.left.addWidget(self.facture_table)
        self.left.addLayout(self.down)

        self.upc_input = QLineEdit()
        self.upc_input.setPlaceholderText("UPC")
        self.add = QPushButton("Ajouter UPC")
        self.clear = QPushButton("Vider")

        self.right = QFormLayout()
        self.right.addRow("UPC: ", self.upc_input)
        self.right.addRow(self.add)
        self.right.addRow(self.clear)
        self.right.setFieldGrowthPolicy(QFormLayout.FieldsStayAtSizeHint)

        self.layout = QHBoxLayout()
        #self.layout.addWidget(self.facture_table)
        self.layout.addLayout(self.left)
        self.layout.addLayout(self.right)
        self.setLayout(self.layout)
        self.facture_table.resizeColumnsToContents()

        self.set_behavior()
    
    def set_behavior(self):
        self.add.clicked.connect(self.add_upc)
        self.clear.clicked.connect(self.clear_facture)
        self.facture_model.layoutChanged.connect(self.update_total)
        self.facture_model.dataChanged.connect(self.update_total)

    def add_upc(self):
        upc = self.upc_input.text()
       
        # Check if upc is valid
        if len(upc) != 12 or not upc.isdigit() or not self.facture_model.add_upc(upc):
            show_error_dialog("UPC invalide ou non existant")
        else:
            self.upc_input.setText("")
                 
    def clear_facture(self):
        self.facture_model.clear_facture()
        # self.update_total()

    def update_total(self):
        self.facture_total.setText(self.facture_model.get_total() + "  $") 

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