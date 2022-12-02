import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    port=3306,
    database='HospitalManagement',
    user="root",
    password="1234"
)

my_cursor = mydb.cursor(buffered=True)


