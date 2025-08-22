import mysql.connector

conn = mysql.connector.connect(
    host = 'localhost',
    user = 'devuser',
    password = 'Shivam@123',
    database = 'expensedb'
)

cursor = conn.cursor()

cursor.execute("SELECT item,amount FROM expenses")
results = cursor.fetchall()

if results:
    print("Your expenses: ")
    for item,amount in results:
        print(f"{item}: Rs {amount}")
else:
    print("No expenses found")

cursor.close()
conn.close()
