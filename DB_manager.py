import mysql.connector
from mysql.connector import errorcode
from datetime import datetime


class DatabaseUtility:
    def __init__(self, database):
        self.db = database

        p='madagascar'
        self.cnx = mysql.connector.connect(user='root',
                                           password=p,
                                           host='127.0.0.1')

        self.cnx.autocommit = True
        self.cursor = self.cnx.cursor()

        self.ConnectToDatabase()

    def ConnectToDatabase(self):
        try:
            self.cnx.database = self.db
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                self.CreateDatabase()
                self.cnx.database = self.db
            else:
                print(err.msg)

    def CreateDatabase(self):
        try:
            self.RunCommand("CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8';".format(self.db))
        except mysql.connector.Error as err:
            print("Failed creating database: {}".format(err))

    def CreateTable(self, tableName):
        cmd = (" CREATE TABLE IF NOT EXISTS " + tableName + " ("
                                                                 " `ID` int(5) NOT NULL AUTO_INCREMENT,"
                                                                 " `date` date NOT NULL,"
                                                                 " `time` time NOT NULL,"
                                                                 " `message` char(50) NOT NULL,"
                                                                 " PRIMARY KEY (`ID`)"
                                                                 ") ENGINE=InnoDB;")
        self.RunCommand(cmd)

    def GetTable(self, tableName, data):
        return self.RunCommand("SELECT * FROM %s;" % tableName)

    def GetColumns(self, tableName):
        return self.RunCommand("SHOW COLUMNS FROM %s;" % tableName)

    def RunCommand(self, cmd):
        print("RUNNING COMMAND: " + cmd)
        try:
            self.cursor.execute(cmd)
        except mysql.connector.Error as err:
            print('ERROR MESSAGE: ' + str(err.msg))
            print('WITH ' + cmd)
        try:
            msg = self.cursor.fetchall()
        except:
            msg = self.cursor.fetchone()
        return msg

    def AddEntryToTable(self, tableName, message):
        date1 = datetime.now().strftime("%y-%m-%d")
        time = datetime.now().strftime("%H:%M")

        cmd = " INSERT INTO " + tableName + " (date, time, message)"
        cmd += " VALUES ('%s', '%s', '%s' );" % (date1, time, message)
        self.RunCommand(cmd)

    def AddRecordToTable(self, tableName, data):
        cmd = " INSERT INTO " + tableName + " (first_name, middle_name, last_name, sex, age)"
        cmd += " VALUES ('%s', '%s', '%s', '%s', '%d');" % data
        self.RunCommand(cmd)

    def Query(self, tableName, data):
        cmd = []
        for k in data:
            cmd.append(k + " LIKE '" + data[k] + "%'")
            # cmd.append(k + " LIKE '" + data[k][0] + '_'*(len(data[k])-2) + data[k][-1] + "'")
        cmd = "SELECT * FROM " + tableName + " WHERE " + " AND ".join(cmd) + ";"

        return self.RunCommand(cmd)

    def AddToQueue(self, tableName, data):
        cmd = " INSERT INTO " + tableName + " (p_id) "
        cmd += "VALUES ('" + data + "');"
        self.RunCommand(cmd)

    def FetchQueue(self, idTable, visitTable):
        cmd = f"SELECT p_id AS SNo, CONCAT(first_name, ' ', middle_name, ' ', last_name) AS NAME" \
              " FROM {idTable}, {visitTable} WHERE ongoing = TRUE" \
              " AND {idTable}.patient_id = {visitTable}.p_id;"
        self.RunCommand(cmd)

    def __del__(self):
        self.cnx.commit()
        self.cursor.close()
        self.cnx.close()


if __name__ == '__main__':
    db = 'myFirstDB'
    tableName = 'test8'

    dbu = DatabaseUtility(db)

    print(dbu.GetColumns())
# dbu.AddEntryToTable('testing')
# dbu.AddEntryToTable('testing2')
# print(dbu.GetTable())

