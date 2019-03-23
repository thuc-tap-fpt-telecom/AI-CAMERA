import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="orangepi123"
)

mycursor = mydb.cursor()

mycursor.execute("CREATE DATABASE mydatabase")