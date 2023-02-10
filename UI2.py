FREECADPATH = 'C:\Program Files\FreeCAD 0.20\\bin'
import sys
import json
sys.path.append(FREECADPATH)
from PyQt5 import QtWidgets, QtGui, QtCore
import FreeCAD
import FreeCADGui


class TreeWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # create a menu bar
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("&File")
        view_menu = menu_bar.addMenu("&View")
        

        self.form_dock = QtWidgets.QDockWidget("Form")

        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.form_dock)
        self.dock_layout = QtWidgets.QVBoxLayout(self)

        def getMainWindow():
            toplevel = QtWidgets.qApp.topLevelWidgets()
            for i in toplevel:
                if i.metaObject().className() == "Gui::MainWindow":
                    return i
            raise Exception("No main window found")
        
        freecadDMU = FreeCADGui.showMainWindow()
        freecadDMU = getMainWindow()
        

        self.dmu_dock = QtWidgets.QDockWidget("DMU")
        self.dmu_dock.setWidget(freecadDMU)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.dmu_dock)

        # create actions to add to the menu bar
        show_dmu_action = QtWidgets.QAction("Show DMU", self)
        show_dmu_action.setCheckable(True)
        show_dmu_action.setChecked(True)
        show_dmu_action.setShortcut('F1')
        show_dmu_action.triggered.connect(self.toggle_dmu)
        view_menu.addAction(show_dmu_action)

        # create actions to add to the menu bar
        show_form_action = QtWidgets.QAction("Show Form", self)
        show_form_action.setCheckable(True)
        show_form_action.setChecked(True)
        show_form_action.setShortcut('F2')
        show_form_action.triggered.connect(self.toggle_form)
        view_menu.addAction(show_form_action)

        # Open => Open file
        openFile = QtWidgets.QAction("Open file", self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Open FreeCAD Model')
        openFile.triggered.connect(self.showPart)
        file_menu.addAction(openFile)
        
        # Save
        save = QtWidgets.QAction("Save", self)
        file_menu.addAction(save)

        # Save As
        save_as = QtWidgets.QAction("Save as", self)
        file_menu.addAction(save_as)

        # liste pour afficher les parties sélectionnées
        self.partList = QtWidgets.QListWidget(self)
        self.partList.itemClicked.connect(self.displayPart)

        # widget texte pour afficher les info sur la partie sélectionnée
        self.infoBox = QtWidgets.QTextEdit(self)
        self.infoBox.setReadOnly(True)


        self.tree = QtWidgets.QTreeWidget()
        self.tree.setHeaderLabels(["Instructions"])
        self.root = QtWidgets.QTreeWidgetItem(self.tree, ["Instruction 1"])
        self.tree.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.tree.customContextMenuRequested.connect(self.context_menu)
        self.tree.itemClicked.connect(self.open_form)
        

        self.button_gp = QtWidgets.QPushButton("Generate procedure ",self)
        self.button_gp.clicked.connect(self.generate_procedure)

        # Add the widget to the layout        
        self.tree_layout = QtWidgets.QGridLayout()
        self.tree_layout.addWidget(self.tree)
        self.tree_layout.addWidget(self.button_gp)
        self.tree_layout.addWidget(self.partList)
        self.tree_layout.addWidget(self.infoBox)
        

        self.tree_widget = QtWidgets.QWidget()
        self.tree_widget.setLayout(self.tree_layout)
        self.setCentralWidget(self.tree_widget)
     
    def generate_procedure(self):
        QtWidgets.QMessageBox.about(self, "Title", "Procedure succesfuly generated")

    def open_form(self, item):
        # Get the selected item's text
        selected_text = item.text(0)

        # Create a form widget to display
        form = QtWidgets.QWidget()
        form.setWindowTitle("Form for " + selected_text)

        self.entity_combo = QtWidgets.QComboBox()
        self.entity_combo.addItems(["Nut", "Entité 2", "Entité 3"])

        self.action_combo = QtWidgets.QComboBox()
        self.action_combo.addItems(["Torque", "Action 2", "Action 3"])

        # Add a layout to the form
        form_layout = QtWidgets.QFormLayout()
        label1 = QtWidgets.QLabel("Form for " + selected_text)
        form_layout.addWidget(label1)
        form_layout.addRow("Entité", self.entity_combo)
        form_layout.addRow("Action", self.action_combo)

        button1 = QtWidgets.QPushButton("Preview instruction ", self)
        label2 = QtWidgets.QLabel("Preview for " + selected_text)
        form_layout.addWidget(label2)        
        form_layout.addWidget(button1)
        button1.pressed.connect(self.find)

        # Create a preview widget to display
        self.preview = QtWidgets.QTextEdit()
        self.preview.setWindowTitle("Preview for " + selected_text)
        form_layout.addWidget(self.preview)
        form.setLayout(form_layout)
    
        # Set the form widget as the central widget for the form dock
        self.form_dock.setWidget(form)
    
    def find(self):
        entity_text = self.entity_combo.currentText()
        action_text = self.action_combo.currentText()
        self.preview.setText(action_text + ' the ' + entity_text)


    def toggle_form(self):
        if self.form_dock.isVisible():
            self.form_dock.hide()
        else:
            self.form_dock.show() 

    def toggle_dmu(self):
        if self.dmu_dock.isVisible():
            self.dmu_dock.hide()
        else:
            self.dmu_dock.show()    

    def context_menu(self, point):
        selected = self.tree.selectedItems()[0]
        menu = QtWidgets.QMenu()
        add_child_action = menu.addAction("Add Child")
        add_child_action.triggered.connect(self.add_child)
        add_sibling_action = menu.addAction("Add Sibling")
        add_sibling_action.triggered.connect(self.add_sibling)
        delete_action = menu.addAction("Delete")
        delete_action.triggered.connect(self.delete)

        menu.exec_(self.tree.viewport().mapToGlobal(point))

    def delete(self):
        selected = self.tree.selectedItems()[0]
        reply = QtWidgets.QMessageBox.question(self.tree, "Delete", "Are you sure you want to delete the selected item and its child items?",
                                            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            for item in self.tree.selectedItems():
                (item.parent() or selected).removeChild(item)
 
        
    def add_child(self):
        selected = self.tree.selectedItems()[0]
        name, ok = QtWidgets.QInputDialog.getText(self.tree, "Add Item", "Enter name:")
        if ok:
            new_item = QtWidgets.QTreeWidgetItem(selected, [name])
            self.tree.expandItem(selected)

    def add_sibling(self):
        selected = self.tree.selectedItems()[0]
        parent = selected.parent()
        name, ok = QtWidgets.QInputDialog.getText(self.tree, "Add Item", "Enter name:")
        if parent:
            if ok:
                new_item = QtWidgets.QTreeWidgetItem(parent, [name])
        else:
            if ok:
                new_item = QtWidgets.QTreeWidgetItem(self.tree, [name])

    def showPart(self):
        # ouvre un fichier FreeCAD
        filename = QtWidgets.QFileDialog.getOpenFileName(self)
        FreeCAD.open(filename[0])
        # récupère les parties du modèle et les ajouter à une liste
        parts = FreeCAD.ActiveDocument.Objects
        self.partList.clear()
        for part in parts:
            item = QtWidgets.QListWidgetItem(part.Name)
            self.partList.addItem(item)

    def displayPart(self, item):
        # récupère les info sur la partie sélectionnée
        selectedPart = FreeCAD.ActiveDocument.getObject(item.text())
        info = 'Name: ' + selectedPart.Name + '\n'
        info += 'Shape Type: ' + selectedPart.Shape.ShapeType + '\n'
        info += 'Volume: ' + str(selectedPart.Shape.Volume) + '\n'
        # affiche les info
        self.infoBox.setText(info)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = TreeWindow()
    main_window.showMaximized()

    sys.exit(app.exec_())
