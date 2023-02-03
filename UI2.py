FREECADPATH = 'C:\Program Files\FreeCAD 0.20\\bin'
import sys
sys.path.append(FREECADPATH)
from PyQt5 import QtWidgets, QtGui, QtCore
import FreeCADGui



class TreeWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.tree = QtWidgets.QTreeWidget()
        self.tree.setHeaderLabels(["Instructions"])

        # create a menu bar
        menu_bar = self.menuBar()
        view_menu = menu_bar.addMenu("View")

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
        show_dmu_action.triggered.connect(self.toggle_dmu)
        view_menu.addAction(show_dmu_action)

        self.root = QtWidgets.QTreeWidgetItem(self.tree, ["Instruction 1"])
        self.tree.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.tree.customContextMenuRequested.connect(self.context_menu)

        tree_layout = QtWidgets.QVBoxLayout()
        tree_layout.addWidget(self.tree)


        self.tree_widget = QtWidgets.QWidget()
        self.tree_widget.setLayout(tree_layout)
        self.setCentralWidget(self.tree_widget)

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
        menu.exec_(self.tree.viewport().mapToGlobal(point))

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

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    main_window = TreeWindow()
    main_window.showMaximized()

    sys.exit(app.exec_())
