import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user='root',
    passwd='madagascar',
    database='testdb'
)

mycursor = mydb.cursor()

# mycursor.execute("CREATE TABLE students (name VARCHAR(255), age INTEGER(10))")

sqlFormula = "INSERT INTO students (name, age) VALUES (%s, %s)"
student1 = [('Bob', 12),
            ('Amanda', 32),
            ('Jacob', 21),
            ('Avi', 28),
            ('Michelle', 17)]

mycursor.executemany(sqlFormula, student1)

mydb.commit()