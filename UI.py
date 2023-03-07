FREECADPATH = r'C:\Users\agrihon\AppData\Local\Programs\FreeCAD 0.20\bin'
import sys
import json
sys.path.append(FREECADPATH)
from PyQt5 import QtWidgets, QtGui, QtCore
import FreeCAD
import FreeCADGui

class TreeWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.hideList = []

        self.entity_form = {}
        # Window style
        self.originalPalette = QtWidgets.QApplication.palette()

        # create a menu bar
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("&File")
        view_menu = menu_bar.addMenu("&View")
        
        self.form_dock = QtWidgets.QDockWidget("Form")

        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.form_dock)
        #self.dock_layout = QtWidgets.QVBoxLayout(self)

        def getMainWindow():
            toplevel = QtWidgets.qApp.topLevelWidgets()
            for i in toplevel:
                if i.metaObject().className() == "Gui::MainWindow":
                    return i
            raise Exception("No main window found")
        
        freecadDMU = FreeCADGui.showMainWindow()
        freecadDMU = getMainWindow()

        dockWidgets = freecadDMU.findChildren(QtWidgets.QDockWidget)
        for dw in dockWidgets:
            if dw.objectName() == "Python console":
                pcWidget = dw
                pcWidget.hide()
            if dw.objectName() == "Combo View":
                cvWidget = dw
                # cvWidget.setVisible(False)
            if dw.objectName() == "Report view":
                rvWidget = dw
                rvWidget.hide()

        toolWidgets = freecadDMU.findChildren(QtWidgets.QToolBar)
        for tw in toolWidgets:
            tw.hide()

        # create procedure dock
        self.Fullpreview = QtWidgets.QTextEdit()
        self.Fullpreview.setReadOnly(True)
        self.Fullpreview_dock = QtWidgets.QDockWidget('Procedure')
        self.Fullpreview_dock.setWidget(self.Fullpreview)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.Fullpreview_dock)
        
        # Desactivate panels in FreeCAD (autre méthode)
        # self.report_view = freecadDMU.findChild(QtWidgets.QDockWidget, "Python console")
        # if self.report_view is not None:
        #     self.report_view.setVisible(False)

        # create dmu dock
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

        # # Entity list widget
        # self.partList = QtWidgets.QListWidget(self)
        # self.partList.setWindowTitle("Liste")
        # self.partList.itemClicked.connect(self.displayPart)

        # # Info entity widget
        # self.infoBox = QtWidgets.QTextEdit(self)
        # self.infoBox.setReadOnly(True)

        # Instruction list widget
        self.tree = QtWidgets.QTreeWidget()
        self.tree.setHeaderLabels(["Instructions"])
        self.root = QtWidgets.QTreeWidgetItem(self.tree, ["Instruction 1"])
        self.tree.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.tree.customContextMenuRequested.connect(self.context_menu)
        self.tree.itemClicked.connect(self.open_form)
        
        # Generate procedure button
        self.button_gp = QtWidgets.QPushButton("Generate procedure",self)
        self.button_gp.clicked.connect(self.generate_procedure)

        # Show/Hide selection button
        self.button_ds = QtWidgets.QPushButton("Show/Hide selected entity",self)
        self.button_ds.clicked.connect(self.deactivate_selection)

        # Reset selection button
        self.button_show_all = QtWidgets.QPushButton("Show all",self)
        self.button_show_all.clicked.connect(self.show_all)

        # Add the widget to the layout        
        self.tree_layout = QtWidgets.QGridLayout()
        self.tree_layout.addWidget(self.tree)
        self.tree_layout.addWidget(self.button_gp)
        self.tree_layout.addWidget(self.button_ds)
        self.tree_layout.addWidget(self.button_show_all)
        # self.tree_layout.addWidget(self.partList)
        # self.tree_layout.addWidget(self.infoBox)

        self.tree_widget = QtWidgets.QWidget()
        self.tree_widget.setLayout(self.tree_layout)
        self.setCentralWidget(self.tree_widget)

        # Define window style (window or fusion)
        QtWidgets.QApplication.setStyle(QtWidgets.QStyleFactory.create('Fusion'))

# WIP Tree Save :

    # def closeEvent(self, event):
    #     self.save_tree_state()

    # def save_tree_state(self):
    #     state = self.treeToJson(self.tree)
    #     with open(self.tree_file_path, 'w') as file:
    #         json.dump(state, file)
    
    # def load_tree_state(self):
    #     try:
    #         with open(self.tree_file_path, 'r') as file:
    #             state = json.load(file)
    #             self.jsonToTree(state, self.tree)
    #     except FileNotFoundError:
    #         pass

    # def treeToJson(self, tree):
    #     state = {}
    #     for index in range(tree.topLevelItemCount()):
    #         item = tree.topLevelItem(index)
    #         state[item.text(0)] = self.itemToJson(item)
    #     return state

    # def itemToJson(self, item):
    #     state = {'text': item.text(0)}
    #     for index in range(item.childCount()):
    #         child = item.child(index)
    #         state.setdefault('children', []).append(self.itemToJson(child))
    #     return state

    # def jsonToTree(self, state, tree):
    #     for key, value in state.items():
    #         item = QtWidgets.QTreeWidgetItem([value['text']])
    #         tree.addTopLevelItem(item)
    #         if 'children' in value:
    #             self.jsonToItem(value['children'], item)

    # def jsonToItem(self, state, parent):
    #     for value in state:
    #         item = QtWidgets.QTreeWidgetItem([value['text']])
    #         parent.addChild(item)
    #         if 'children' in value:
    #             self.jsonToItem(value['children'], item)
#

    def generate_procedure(self):
        QtWidgets.QMessageBox.about(self, "Title", "Procedure succesfuly generated")

    def open_form(self, item):

        # Get the selected item's text
        self.selected_text = item.text(0)
        print(self.entity_form)

        # Check if form widget for selected entity already exists   
        if self.selected_text in self.entity_form:
            # form already exists, just show it
            self.form_dock.setWidget(self.entity_form[self.selected_text])
            self.action_combo.currentIndexChanged.connect(self.save_data)
        else:

            # Form widget to display
            form = QtWidgets.QWidget()

            # Separation line
            line = QtWidgets.QFrame()
            line.setFrameStyle(QtWidgets.QFrame.HLine | QtWidgets.QFrame.Sunken)

            # Form title
            self.label1 = QtWidgets.QLabel("Form for " + self.selected_text)

            # Entity combo box
            self.entity_combo = QtWidgets.QComboBox()
            self.entity_combo.addItem("Select an entity...")
            self.entity_combo.addItems(["Bolt (11)", "Washer (12)", "Fuselage attachement bracket (15)"])
            self.entity_combo.activated.connect(self.enable_action_combo)


            # Get entity button
            self.get_selection_button = QtWidgets.QPushButton("Get 3D entity selection")
            self.get_selection_button.clicked.connect(self.get_selection)

            # Entity line
            self.hentity  = QtWidgets.QHBoxLayout()
            self.hentity.addWidget(self.entity_combo)
            self.hentity.addWidget(self.get_selection_button)
            self.hentity.addStretch()

            # Action combo box
            self.action_combo = QtWidgets.QComboBox()
            self.action_combo.addItems(["Torque", "Remove", "Disconnect"])
            self.action_combo.setEnabled(False)
            self.action_combo.activated.connect(self.enable_button_preview)
            self.action_combo.adjustSize()

            # Action line
            self.haction = QtWidgets.QHBoxLayout()
            self.haction.addWidget(self.action_combo)
            self.haction.addStretch()

            # Preview part
            self.label2 = QtWidgets.QLabel("Preview for: " + self.selected_text)
            self.button_preview = QtWidgets.QPushButton("Preview for: ", self)
            self.button_preview.setEnabled(False)
            self.action_combo.currentIndexChanged.connect(self.find)
            hbox2 = QtWidgets.QHBoxLayout()
            hbox2.addWidget(self.button_preview)
            hbox2.addStretch()
            self.preview = QtWidgets.QTextEdit()
            self.preview.setReadOnly(True)

            # Form layout
            form_layout = QtWidgets.QFormLayout()
            form_layout.addWidget(self.label1)
            form_layout.addRow("Entity", self.hentity)
            form_layout.addRow("Action", self.haction)
            form_layout.addRow(line)
            form_layout.addWidget(self.label2)
            form_layout.addRow(self.preview)

            form.setLayout(form_layout)
            
            # Add the form widget to the dictionary
            self.entity_form[self.selected_text] = form

            # Set the form widget as the central widget for the form dock
            self.form_dock.setWidget(form)

            self.action_combo.currentIndexChanged.connect(self.save_data)

    def save_data(self):
        data = {
            'Title' : self.label1.text(),
            'Entity': self.entity_combo.currentText(),
            'Action': self.action_combo.currentText(),
        }
        with open(self.label1.text()+'.json', 'w') as f:
            json.dump(data, f, indent=4)

    def enable_action_combo(self):
        if self.entity_combo.currentText() == "Select an entity...":
            self.action_combo.setEnabled(False)
        else:
            self.action_combo.setEnabled(True)

    def enable_button_preview(self):
        self.button_preview.setEnabled(True)

    def get_selection(self):
        selection = FreeCADGui.Selection.getSelection()
        if selection:
            selected_object = selection[0]
            print("Selected entity : ", selected_object.Label)
            # self.entity_combo.addItems([selected_object.Label])
            self.entity_combo.setItemText(0, selected_object.Label)
            self.action_combo.setEnabled(True)

        else:
            print("No object selected")

    def deactivate_selection(self):
        selection = FreeCADGui.Selection.getSelection()
        if selection:
            selected_object = selection[0]
            if selected_object.ViewObject.Visibility == True:
                selected_object.ViewObject.Visibility = False
                # Add entity to a list for show_all function
                self.hideList.append(selected_object)
            else:
                selected_object.ViewObject.Visibility = True
        else:
            print("No selected entity")

    def show_all(self):
        if len(self.hideList) != 0 :
            for entity in self.hideList:
                entity.ViewObject.Visibility = True
            self.hideList.clear()

    def find(self):
        entity_text = self.entity_combo.currentText()
        action_text = self.action_combo.currentText()
        self.preview.setText(action_text + ' the ' + entity_text)
        text = self.entity_combo.currentText() + " | " + self.action_combo.currentText()
        self.label1.setText("Form for: " + text)
        self.label2.setText("Preview for: " + text)

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
        try:
            # ouvre un fichier FreeCAD
            filename = QtWidgets.QFileDialog.getOpenFileName(self)
            FreeCAD.open(filename[0])
            # récupère les parties du modèle et les ajouter à une liste
            parts = FreeCAD.ActiveDocument.Objects
            self.partList.clear()
            for part in parts:
                item = QtWidgets.QListWidgetItem(part.Name)
                self.partList.addItem(item)
        except:
            print("No file selected")

    def displayPart(self, item):
        # récupère les info sur la partie sélectionnée
        selectedPart = FreeCAD.ActiveDocument.getObject(item.text())
        info = 'Name: ' + selectedPart.Name + '\n'
        try :
            info += 'Shape Type: ' + selectedPart.Shape.ShapeType + '\n'
        except :
            info += 'Shape Type: no shape type' + '\n'
        try :
            info += 'Volume: ' + str(selectedPart.Shape.Volume) + '\n'
        except :
            info += 'Volume: no volume' + '\n'
        # Afficher les info
        self.infoBox.setText(info)

    # def save_to_json(self):
    #     file_path, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save file", "", "JSON Files (*.json)")
    #     if file_path:
    #         data = {}
    #         root_item = self.treeModel.invisibleRootItem()
    #         for i in range(root_item.rowCount()):
    #             key_item = root_item.child(i, 0)
    #             value_item = root_item.child(i, 1)
    #             key = key_item.text()
    #             value = value_item.text()
    #             data[key] = value

    #         form_data = {}
    #         for i in range(self.formLayout.rowCount()):
    #             key_widget = self.formLayout.itemAt(i, QtWidgets.QFormLayout.LabelRole).widget()
    #             value_widget = self.formLayout.itemAt(i, QtWidgets.QFormLayout.FieldRole).widget()
    #             key = key_widget.text()
    #             value = value_widget.text()
    #             form_data[key] = value

    #         with open(file_path, 'w') as f:
    #             json.dump({"tree": data, "form": form_data}, f)
    
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = TreeWindow()
    main_window.showMaximized()

    sys.exit(app.exec_())