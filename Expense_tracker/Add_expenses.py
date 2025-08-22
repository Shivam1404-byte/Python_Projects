import mysql.connector

#connect to SQL
conn = mysql.connector.connect(
    host="localhost",
    user="devuser",
    password="Shivam@123",
    database="expensedb"
)

cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS expenses(
               ID INT AUTO_INCREMENT PRIMARY KEY,
               item VARCHAR(255),
               amount DECIMAL(10,2)
               )
""")

item = input("What did you spend the money on? : ")
amount = float(input("Enter the amount you spend : "))

cursor.execute("INSERT INTO expenses (item,amount) VALUES (%s,%s)",(item,amount))
conn.commit()

print("Expenses save in database")

cursor.close()
conn.close()