import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user='root',
    passwd='madagascar',
    database='testdb'
)

mycursor = mydb.cursor()

# mycursor.execute("CREATE TABLE students (name VARCHAR(255), age INTEGER(10))")

# sqlFormula = "INSERT INTO students (name, age) VALUES (%s, %s)"

# CREATE
# USE
# SELECT
# WHERE
# LIKE

sql = "SELECT * FROM students WHERE name LIKE '%ac%'"

mycursor.execute(sql)

myresult = mycursor.fetchall()

for row in myresult:
    print(row)
