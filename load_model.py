"""@package data_structure.case_model

File that contains the class CaseModel that creates a model for the Case treeview list.

"""
from PyQt4 import QtCore, QtGui



class LoadModel(QtCore.QAbstractItemModel):
    """
    This is a creation of a model for the tree view list.

    It inherits the basic QAbstractItemModel classThe QAbstractItemModel class defines the standard interface that
    item models must use to be able to inter-operate with other components in the model/view architecture. It is not
    supposed to be instantiated directly. Instead, you should subclass it to create new models. This model will be
    the one used by a a data_structure.case_node.LoadNode object.
a
    When subclassing QAbstractItemModel, at the very least you must implement index(), parent(), rowCount(),
    columnCount(), and data(). These functions are used in all read-only models, and form the basis of editable
    models. More info: http://doc.qt.io/qt-5/qabstractitemmodel.html#details

    """

    def __init__(self, root, parent=None):
        super(LoadModel, self).__init__(parent)
        self._rootNode = root

    def rowCount(self, parent):
        """
        Returns the number of rows under the given parent. When the parent is valid it means that rowCount is returning
        the number of children of parent.

        """
        if not parent.isValid():
            parent_node = self._rootNode
        else:
            parent_node = parent.internalPointer()

        return parent_node.childCount()

    def columnCount(self, parent):
        """
        Returns the number of columns for the children of the given parent.
        ref: http://pyqt.sourceforge.net/Docs/PyQt4/qabstractitemmodel.html#columncount

        """
        return 5

    def data(self, index, role):
        """
        Returns the data stored under the given role for the item referred to by the index.
        """
        if not index.isValid():
            return None

        node = index.internalPointer()

        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
            if index.column() == 0:
                return node.load_type

            if index.column() == 1:
                return node.load_1

            if index.column() == 2:
                return node.pos_1

            if index.column() == 3:
                return node.load_2

            if index.column() == 4:
                return node.pos_2


    def setData(self, index, value, role=QtCore.Qt.EditRole):
        """
        Sets the role data for the item at index to value.
        ref: http://pyqt.sourceforge.net/Docs/PyQt4/qabstractitemmodel.html#setdata

        """
        if index.isValid():

            node = index.internalPointer()

            if role == QtCore.Qt.EditRole:


                if index.column() == 1:
                    node.load_1 = value

                if index.column() == 2:
                    node.pos_1 = value

                if node.load_type == "Distr. Load":
                    if index.column() == 3:
                        node.load_2 = value

                    if index.column() == 4:
                        node.pos_2 = value


                self.dataChanged.emit(index, index)
                return True

        return False

    def headerData(self, section, orientation, role):
        """
        Returns the data for the given role and section in the header with the specified orientation.
        http://pyqt.sourceforge.net/Docs/PyQt4/qabstractitemmodel.html#headerdata
        """
        if role == QtCore.Qt.DisplayRole:
            if section == 0:
                return "Load Type"
            elif section == 1:
                return "Start Load"
            elif section == 2:
                return "Start Pos"
            elif section == 3:
                return "End Load"
            elif section == 4:
                return "End Pos"

    def flags(self, index):
        """
        Returns the item flags for the given index.
        ref: http://pyqt.sourceforge.net/Docs/PyQt4/qabstractitemmodel.html#flags

        """
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable

    def parent(self, index):
        """
        Returns the parent of the model item with the given index.
        ref: http://pyqt.sourceforge.net/Docs/PyQt4/qabstractitemmodel.html#parent

        """

        node = self.getNode(index)
        parent_node = node.parent()

        if parent_node == self._rootNode:
            return QtCore.QModelIndex()

        return self.createIndex(parent_node.row(), 0, parent_node)

    def index(self, row, column, parent):
        """
        Returns the index of the item in the model specified by the given row, column and parent index.
        ref: http://pyqt.sourceforge.net/Docs/PyQt4/qabstractitemmodel.html#index

        """

        parent_node = self.getNode(parent)
        child_item = parent_node.child(row)

        if child_item:
            return self.createIndex(row, column, child_item)
        else:
            return QtCore.QModelIndex()

    def getNode(self, index):

        if index.isValid():
            node = index.internalPointer()
            if node:
                return node
        return self._rootNode

    def removeRows(self, position, rows, parent=QtCore.QModelIndex()):
        """
        Method for removing rows from the data structure
        ref: http://pyqt.sourceforge.net/Docs/PyQt4/qabstractitemmodel.html#removeows

        """
        parent_node = self.getNode(parent)
        self.beginRemoveRows(parent, position, position + rows - 1)

        for row in range(rows):
            success = parent_node.removeChild(position)

        self.endRemoveRows()

        return success


class LoadNode(object):

    def __init__(self, load_type, load_1=None, pos_1=None, load_2=None, pos_2=None, parent=None):

        super(LoadNode, self).__init__()

        if parent is not None:
            self.subshape = []
            self.load_type = load_type
            self.load_1 = load_1
            self.load_2 = load_2
            self.pos_1 = pos_1
            self.pos_2 = pos_2
            self._parent = parent


            parent.addChild(self)

        self._children = []

    # Below is defining the methods for getting and setting protected members of the class.

    def addChild(self, child):
        """
        Methods required by model tree view of PyQt. Not necessary to observe this method.
        """
        self._children.append(child)

    def insertChild(self, position, child):
        """
        Methods required by model tree view of PyQt. Not necessary to observe this method.
        """
        if position < 0 or position > len(self._children):
            return False

        self._children.insert(position, child)
        child._parent = self
        return True

    def removeChild(self, position):
        """
        Methods required by model tree view of PyQt. Not necessary to observe this method.
        """
        if position < 0 or position > len(self._children):
            return False

        child = self._children.pop(position)
        child._parent = None

        return True

    # def name(self):
    #     """
    #     Methods required by model tree view of PyQt. Not necessary to observe this method.
    #     """
    #     return self._name
    #
    # def setName(self, name):
    #     """
    #     Methods required by model tree view of PyQt. Not necessary to observe this method.
    #     """
    #     self._name = name

    def child(self, row):
        """
        Methods required by model tree view of PyQt. Not necessary to observe this method.
        """
        return self._children[row]

    @property
    def children(self):
        """
        Methods required by model tree view of PyQt. Not necessary to observe this method.
        """
        return self._children

    def childCount(self):
        """
        Methods required by model tree view of PyQt. Not necessary to observe this method.
        """
        return len(self._children)

    def parent(self):
        """
        Methods required by model tree view of PyQt. Not necessary to observe this method.
        """
        return self._parent

    def row(self):
        """
        Methods required by model tree view of PyQt. Not necessary to observe this method.
        """
        if self.parent() is not None:
            return self.parent().children.index(self)
