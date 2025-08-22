import csv

messy_data = [
    ["Name", "Age", "Salary", "Department"],
    ["John Doe", "25", "50000", "Sales"],
    ["jane smith", "30", "60,000", "Marketing"],
    ["", "35", "70000", "IT"],
    ["Bob Johnson", "abc", "80000", "Sales"],
    ["Alice Brown", "28", "", "Marketing"],
    ["MIKE WILSON", "45", "90,000", "IT"],
    ["sarah davis", "32", "55000", ""],
]

with open("sample_messy_data","w",newline="") as file:
    writer = csv.writer(file)
    writer.writerows(messy_data)

print("Written the messy data")