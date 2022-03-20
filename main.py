import model
import sys
from pathlib import Path
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *

ICON_PATH = Path('data/ulaval_shield.svg')
class MainView(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowIcon(QIcon(ICON_PATH.as_posix()))

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

        # Create widgets
        self.setup_facture_table()
        self.setup_total()
        self.setup_upc_form()

        self.upc_group = QGroupBox("Ajouter UPC manuellement")
        self.upc_group.setLayout(self.upc_form)
        self.total_group = QGroupBox("Total")
        self.total_group.setLayout(self.total_layout)

        self.right = QVBoxLayout()
        self.right.addWidget(self.upc_group)
        self.right.addWidget(self.del_rows_btn)
        self.right.addWidget(self.clear_btn)
        self.right.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.right.addWidget(self.total_group)

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.facture_table)
        self.layout.addLayout(self.right)
        self.layout.setStretch(0, 1)
        self.setLayout(self.layout)

        self.setup_behavior()
    
    def setup_facture_table(self):
        # Create table
        self.facture_model = model.FactureModel()
        self.facture_table = QTableView()
        self.facture_table.setModel(self.facture_model)

        # Set table properties
        self.facture_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.facture_table.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.facture_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.facture_table.setAlternatingRowColors(True)

        # Set column resize modes
        self.facture_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.facture_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Interactive)
        self.facture_table.horizontalHeader().setDefaultSectionSize(300)
    
    def setup_total(self):
        # Create total field
        self.total_layout = QHBoxLayout()
        self.facture_total = QLabel()
        self.total_layout.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.total_layout.addWidget(self.facture_total)
        self.update_total()
    
    def setup_upc_form(self):
        # Create form widgets
        self.upc_input = QLineEdit()
        self.upc_input.setPlaceholderText("Code UPC")
        self.add_btn = QPushButton("Ajouter")
        self.del_rows_btn = QPushButton("Effacer les lignes")
        self.clear_btn = QPushButton("Vider")

        # Add widgets to form
        self.upc_form = QVBoxLayout()
        self.upc_form.addWidget(self.upc_input)
        self.upc_form.addWidget(self.add_btn)


    def setup_behavior(self):
        self.add_btn.clicked.connect(self.add_upc)
        self.clear_btn.clicked.connect(self.clear_facture)
        self.facture_model.layoutChanged.connect(self.update_total)
        self.del_rows_btn.clicked.connect(self.remove_upcs)

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

def create_facture_table():
    pass

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