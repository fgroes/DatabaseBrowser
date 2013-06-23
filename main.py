import sys
from PySide import QtCore, QtGui
from database import Database


class MainWindow(QtGui.QMainWindow):
    
    def __init__(self):
        super(MainWindow, self).__init__()
        self.initUI()
    
    def initUI(self):
        self.setGeometry(200, 200, 640, 480)
        self.menu = self.menuBar()
        self.cw = MainWidget(self)
        self.setCentralWidget(self.cw)
        self.status = self.statusBar()
        self.show()
        
    def setDatabase(self, nameFile):
        self.db = Database(nameFile)
        self.cw.setDatabase(self.db)
        
        
class MainWidget(QtGui.QWidget):
    
    def __init__(self, parent):
        super(MainWidget, self).__init__(parent)
        self.layoutMain = QtGui.QVBoxLayout(self)
        self.layoutDataBrowser = QtGui.QHBoxLayout()
        self.comboTable = QtGui.QComboBox()
        self.comboTable.currentIndexChanged.connect(self.tableChange)
#        self.comboTable.activated.connect(self.tableReload)
        self.buttonNewRecord = QtGui.QPushButton('New Record')
        self.buttonNewRecord.clicked.connect(self.openAddRecordDialog)
        self.buttonDeleteRecord = QtGui.QPushButton('Delete Record')
        self.layoutDataBrowser.addWidget(QtGui.QLabel('Table:'))
        self.layoutDataBrowser.addWidget(self.comboTable)
        self.layoutDataBrowser.addWidget(self.buttonNewRecord)
        self.layoutDataBrowser.addWidget(self.buttonDeleteRecord)
        self.layoutMain.addLayout(self.layoutDataBrowser)
        self.tableView = QtGui.QTableView()        
        self.layoutMain.addWidget(self.tableView)
        self.setLayout = self.layoutMain
        
    def tableChange(self, index):
        self.setTableModel(self.db.tables[index])
        
#    def tableReload(self):
#        self.comboTable.clear()
#        self.comboTable.addItems(self.db.tables)
        
    def setDatabase(self, database):
        self.db = database
        self.setTableModel(self.db.tables[0])
        self.comboTable.addItems(self.db.tables)
        self.comboTable.setCurrentIndex(0)
        
    def setTableModel(self, nameTable):
        model = self.db.getTableModel(nameTable)
        self.tableView.setModel(model)
        #self.tableView.show()
        
    def openAddRecordDialog(self):
        indexTable = self.comboTable.currentIndex()
        fields = self.db.getFields(self.db.tables[indexTable])
        self.wAddRecord = AddRecord(fields)
        self.wAddRecord.applyClicked.connect(self.addRecord)
        
    def addRecord(self, text):
        print(text)
        
            
class AddRecord(QtGui.QWidget):
    
    applyClicked = QtCore.Signal((tuple,))
    
    def __init__(self, fields):
        super(AddRecord, self).__init__()
        self.fields = fields
        self.initUI()
        
    def initUI(self):
        self.mainLayout = QtGui.QVBoxLayout()
        self.layoutFields = QtGui.QGridLayout()
        for i in range(1, self.fields.count()):
            nameField = self.fields.field(i).name()
            label = QtGui.QLabel('{0:s}:'.format(nameField))
            text = QtGui.QLineEdit()
            self.layoutFields.addWidget(label, i, 0, \
                alignment=QtCore.Qt.AlignRight)
            self.layoutFields.addWidget(text, i, 1)
        self.mainLayout.addLayout(self.layoutFields)
        self.buttonApply = QtGui.QPushButton('Apply')
        self.buttonApply.clicked.connect(self.addRecord)
        self.mainLayout.addWidget(self.buttonApply)
        self.setLayout(self.mainLayout)
        self.show()
    
    def addRecord(self):
        self.applyClicked.emit(('this is a test', 10, ))    


def main(nameDatabase):   
    app = QtGui.QApplication(sys.argv)  
    mw = MainWindow()
    mw.setDatabase(nameDatabase)
    sys.exit(app.exec_())


if __name__ == '__main__':
    nameDatabase = '/home/fritzarch/Code/python/DatabaseBrowser/data'
    main(nameDatabase)