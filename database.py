from PySide import QtCore, QtSql


class Database(object):
    
    statusOptions = ['OPEN', 'CLOSED', 'ERROR']
    
    def __init__(self, name):
        self.connection = QtSql.QSqlDatabase('QSQLITE')
        self.connection.setDatabaseName(name)
        if not self.connection.open():
            print('connection error')
            self._status = 2
        else:
            self._status = 0
            
    def getStatus(self):
        return self.statusOptions[self._status]
        
    status = property(getStatus)
                       
    def getTables(self):
        return self.connection.tables()
        
    tables = property(getTables)
    
    def getFields(self, nameTable):
        return self.connection.record(nameTable)
        
    def __del__(self):
        self.connection.close()
        
    def getTableModel(self, nameTable):
        model = QtSql.QSqlTableModel(db=self.connection)
        model.setTable(nameTable)
        model.setEditStrategy(QtSql.QSqlTableModel.OnFieldChange)
        model.select()
        model.removeColumn(0)
        return model


def main():
    nameDatabase = '/home/fritzarch/Code/python/DataBaseBrowser/data'
    db = Database(nameDatabase)
    print(db.status)
    for t in db.getTables():
        print(t)


if __name__ == '__main__':
    main()