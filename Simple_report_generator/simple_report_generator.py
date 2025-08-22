import csv

employees = []
with open("cleaned_sample_data.txt","r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        employees.append(row)

total_employees = len(employees)
total_salary = sum(int(emp['Salary']) for emp in employees if emp['Salary']!=0)
avg_salary = total_salary/total_employees if total_employees > 0 else 0

dept_counts = {}
for emp in employees:
    dept = emp['Department']
    dept_counts[dept] = dept_counts.get(dept,0) + 1

report = f"""
EMPLOYEE ANALYSIS REPORT 
-------------------------
-------------------------

Total employees : {total_employees}
Average salary : {avg_salary}
Total Payroll : {total_salary}

Employees by department : 
"""

for dept,count in dept_counts.items():
    report+= f"{dept}:{count} employees\n"

with open("Employees_report.txt","w") as file:
    file.write(report)

print("Report generated! Check Employees_report")
print(report)