import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user='root',
    passwd='madagascar',
    database='testdb'
)

mycursor = mydb.cursor()

mycursor.execute("CREATE TABLE student ("
                 "first_name VARCHAR(30) NOT NULL,"
                 "last_name VARCHAR(30) NOT NULL,"
                 "email VARCHAR(60) NULL,"
                 "street VARCHAR(50) NOT NULL,"
                 "city VARCHAR(40) NOT NULL,"
                 "state CHAR(2) NOT NULL DEFAULT 'PA',"
                 "zip INT(8) UNSIGNED NOT NULL,"
                 "phone VARCHAR(20) NOT NULL,"
                 "birth_date DATE NOT NULL,"
                 "sex ENUM('M', 'F') NOT NULL,"
                 "date_entered TIMESTAMP,"
                 "lunch_cost FLOAT NOT NULL,"
                 "student_id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY)")

# sqlFormula = "INSERT INTO students (name, age) VALUES (%s, %s)"

# mycursor.execute("SELECT * FROM students ORDER BY name DESC")
# CREATE
# USE
# SELECT
# INSERT INTO
# WHERE, LIKE
# UPDATE
# LIMIT
# ORDER BY, DESC

# sql = "DROP TABLE IF EXISTS student"

# mycursor.execute(sql)

# myresult = mycursor.fetchall()

# student1 = [('Bob', 12),
#             ('Amanda', 32),
#             ('Jacob', 21),
#             ('Avi', 28),
#             ('Michelle', 17)]
#
# mycursor.executemany(sqlFormula, student1)

# for row in myresult:
#     print(row)
mydb.commit()
mycursor.close()
mydb.close()