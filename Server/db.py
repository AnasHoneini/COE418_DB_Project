import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    port=3307,
    database='HospitalManagement',
    user="root",
    password="Anas@1234"
)

my_cursor = mydb.cursor(buffered=True)


