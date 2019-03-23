import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="orangepi123",
  database="mydatabase"
)

mycursor = mydb.cursor()

#create table
#mycursor.execute("CREATE TABLE employees (name VARCHAR(255), address VARCHAR(255))")

#Create primary key on an existing table
#mycursor.execute("ALTER TABLE employees ADD COLUMN id INT AUTO_INCREMENT PRIMARY KEY")

#create database with primary key
mycursor.execute("CREATE TABLE employees (ID INT AUTO_INCREMENT UNIQUE PRIMARY KEY, Name VARCHAR(255), Age INT, Gender VARCHAR(255))")  