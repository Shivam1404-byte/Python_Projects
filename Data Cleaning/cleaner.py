import csv

cleaned_data=[]

with open("sample_messy_data","r") as file:
    reader = csv.reader(file)
    header = next(reader)
    cleaned_data.append(header)

    for row in reader:
        name,age,salary,department = row

        if name.strip():
            name.strip().title()
        else:
            name = "unknown"

        age_clean = ''.join(c for c in age if c.isdigit())
        if not age_clean:
            age_clean = "0"
        
        salary_clean = salary.replace(",","").strip()
        if not salary_clean:
            salary_clean = "0"

        if department.strip():
            department.strip().title()
        else:
            department = "unknown"

        cleaned_data.append([name,age_clean,salary_clean,department])

with open("cleaned_sample_date.txt","w",newline="") as file:
    writer = csv.writer(file)
    writer.writerows(cleaned_data)

print("Data CLeaned! Check the sample_cleaned data")
