import mysql.connector
from mysql.connector import Error
import re
from datetime import datetime

class StudentDB:
    def __init__(self):
        try:
            self.conn = mysql.connector.connect(
                host = "localhost",
                user = "root",
                password = "password",
                database = "school"
            )
            if self.conn.is_connected():
                self.cursor = self.conn.cursor()
                self.create_table()
        except Error as e:
            print("Error while connecting to the Mysql ",e)

    def create_table(self):
        try:
            create_table_query = """
                CREATE TABLE IF NOT EXISTS students(
                    student_id INT AUTO_INCREMENT PRIMARY KEY,
                    first_name VARCHAR(50) NOT NULL,
                    last_name VARCHAR(50) NOT NULL,
                    email VARCHAR(100) UNIQUE,
                    major VARCHAR(100)
                )
            """

            create_table_course = """
                CREATE TABLE IF NOT EXISTS courses(
                    course_id INT AUTO_INCREMENT PRIMARY KEY,
                    course_code VARCHAR(20) UNIQUE NOT NULL, 
                    course_name VARCHAR(50) NOT NULL,
                    credits INT NOT NULL,
                    instructor VARCHAR(100)
                )
            """

            create_table_enrollment = """
                CREATE TABLE IF NOT EXISTS enrollment(
                    enrollment_id INT AUTO_INCREMENT PRIMARY KEY,
                    student_id INT NOT NULL,
                    course_id INT NOT NULL,
                    enrollment_date DATE NOT NULL,
                    grade VARCHAR(2) NULL,
                    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
                    FOREIGN KEY (course_id) REFERENCES courses(course_id) ON DELETE CASCADE,
                    UNIQUE KEY unique_enrollment (student_id,course_id) 
                )
            """

            self.cursor.execute(create_table_query)
            self.cursor.execute(create_table_course)
            self.cursor.execute(create_table_enrollment)
            self.conn.commit()
        except Error as e:
            print("Table not created : ",e)
    
    def isValidName(self,name):
        pattern = r"^[A-Za-z\s&-]+$"
        return bool(re.match(pattern,name))
    
    def isValidEmail(self,email):
        pattern = r'^[\w\.-]+@[\w\.-]+\w+$'
        if re.match(pattern,email):
            return True
        else:
            return False
        
    def isValidDate(self,date):
        try:
            datetime.strptime(date,"%Y-%m-%d")
            return True
        except Error:
            return False
        
    def isValidMajor(self,major):
        pattern = r"\w[A-Za-z\s&-]+$"
        return bool(re.match(pattern,major))
    

    def isValidAlphaNumeric(self,num):
        if num.isalnum():
            return True
        return False
        
    def isValidNumeric(self,num):
        if num.isdigit():
            return True
        return False
    
    def Add_student(self,first_name,last_name,email,major):
        try:          
            query = "INSERT INTO students (first_name,last_name,email,major) VALUES (%s,%s,%s,%s)"
            record = (first_name,last_name,email,major)

            self.cursor.execute(query,record)
            self.conn.commit()
            print("Student Added Successfully")
        except Error as e:
            print("Failed to insert record :",e)

    def Add_courses(self,course_code,course_name,credits,instructor):
        try:
            query = "INSERT INTO courses (course_code,course_name,credits,instructor) VALUES (%s,%s,%s,%s)"
            record = (course_code,course_name,credits,instructor)

            self.cursor.execute(query,record)
            self.conn.commit()
            print("Course added Successfully!")
        except Error as e:
            print("Failed to insert the data : ",e)

    def Add_enrollment(self,student_id,course_id,enrollment_date,grade):
        try:
            query = "INSERT INTO enrollment (student_id,course_id,enrollment_date,grade) VALUES (%s,%s,%s,%s)"
            record = (student_id,course_id,enrollment_date,grade)

            self.cursor.execute(query,record)
            self.conn.commit()
            print("Enrollment added successfully!")
        except Error as e:
            print("Failed to add enrollment :",e)
    
    def View_students(self):
        try:
            query = "SELECT * FROM students"
            self.cursor.execute(query)
            records = self.cursor.fetchall()
            if not records:
                print("No records found in database")
                return
            print("Students Record : ")
            print("-"*80)
            for row in records:
                print(f"ID :{row[0]} Name:{row[1]} {row[2]} E-mail:{row[3]} Major:{row[4]}")
        except Error as e:
            print("Failed to fetch data")

    def View_Courses(self):
        try:
            query = "SELECT * FROM courses"
            self.cursor.execute(query)
            records = self.cursor.fetchall()
            print("Course Details ")
            for row in records:
                print(f"Course Id : {row[0]} Course code : {row[1]} Course Name : {row[2]} Credits :{row[3]} Instructor's name: {row[4]}")
        except Error as e:
            print("Failed to fetch data",e)

    def View_enrollment(self):
        try:
            query="SELECT * FROM enrollment"
            self.cursor.execute(query)
            records = self.cursor.fetchall()
            if not records:
                raise ValueError("No record found")
            for row in records:
                print(f"enrollment ID : {row[0]} Student ID : {row[1]} Course ID : {row[2]} Enrollment Date: {row[3]} Grade: {row[4]}")
        except ValueError as v:
            print(v)
        except Error as e:
            print("Failed to fetch data : ",e)
    
    def Update_students(self,student_id,field,new_value):
        try:
            update_query = f"UPDATE students SET {field} = %s WHERE student_id = %s"
            self.cursor.execute(update_query,(new_value,student_id))
            self.conn.commit()
            
            if self.cursor.rowcount > 0:
                print("Field Update Successfully!")
            else:
                print("No student found from the given ID")

        except Error as e:
            print("Failed to update record : ",e)
    
    def Delete_students(self,student_id):
        try:
            delete_query="DELETE FROM students WHERE student_id = %s"
            self.cursor.execute(delete_query,(student_id,))
            self.conn.commit()

            if self.cursor.rowcount > 0:
                print("The record deleted successfully!")
            else:
                print("No record found in the table")
        except Error as e:
            print("Failed to delete the record : ",e)

    def Search_students(self,search_term):
        try:
            if not search_term.strip():
                raise ValueError("Search term cannot be empty")
                
            if len(search_term) > 50:
                raise ValueError("Search term too long")
                
            if not re.match(r'^[A-Za-z0-9@.\s-]+$',search_term):
                raise ValueError("Seacrh term contains invalid characters")
            search_query="""
                    SELECT * FROM students
                    WHERE first_name LIKE %s OR last_name LIKE %s OR email LIKE %s OR major LIKE %s
                """
            search_pattern = f"%{search_term}%"
            self.cursor.execute(search_query,(search_pattern,search_pattern,search_pattern,search_pattern))
            records = self.cursor.fetchall()
            if not records:
                print("No matching found!")
                return
            print("Search Results : ")
            print("-"*25)
            for row in records:
                print(f"ID : {row[0]} name : {row[1]} {row[2]} E-mail : {row[3]} major : {row[4]}")
            print("-"*25)
        except ValueError as v:
            print("Validation Failed ",v)
        except Error as e:
            print("Search Failed : ",e)

    def get_student_courses(self,student_id):
        try:
            select_query = """SELECT C.course_id,C.course_code,C.course_name,C.credits,E.enrollment_date,E.grade FROM enrollment E 
             JOIN courses C ON C.course_id = E.course_id WHERE E.student_id = %s"""
            self.cursor.execute(select_query,(student_id,))
            records=self.cursor.fetchall()
            if not records:
                print("Student is not enrolled in any courses.")
                return
            print(f"Courses for student ID {student_id}:")
            print("-"*80)
            for row in records:
                grade = row[5] if row[5] is not None else "Not graded"
                print(f"Course ID : {row[0]} Course Name : {row[1]} Credits : {row[2]} Enrollment Date : {row[3]} Grade : {grade}")
            print("-"*80)
        except Error as e:
            print("Failed to retrieve data of student ID : ",e)

    def get_course_students(self,course_id):
        try:
            select_query = """
                SELECT S.student_id,S.first_name,S.last_name,S.email,E.enrollment_date,E.grade FROM enrollment E 
                JOIN students S ON E.student_id = S.student_id WHERE E.course_id = %s
            """
            self.cursor.execute(select_query,(course_id,))
            records = self.cursor.fetchall()
            if not records:
                print("No student found for the course")
                return
            print("Course details ")
            print("-"*80)
            for row in records:
                grade = row[5] if row[5] is not None else "Not graded"
                print(f"Student ID : {row[0]} Student Name : {row[1]} {row[2]} E-mail : {row[3]} Enrollment Date : {row[4]} Grade : {grade}")
            print("-"*80)
        except Error as e:
            print("Failed to retrieve data from courses ",e)

    def Student_and_Course_details(self,student_id):
        try:
            select_query="""
                SELECT S.student_id,S.first_name,S.last_name,C.course_name,S.email,E.enrollment_date,E.grade FROM enrollment AS E JOIN students S ON 
                S.student_id=E.student_id JOIN courses AS C ON C.course_id = E.course_id WHERE S.student_id = %s;
            """
            self.cursor.execute(select_query,(student_id,))
            records = self.cursor.fetchall()
            if not records:
                print("No Students found")
                return
            print("Student Details : ")
            print("-"*80)
            for row in records:
                grade = row[6] if row[6] is not None else "Not graded"
                print(f"Student ID : {row[0]} Name:{row[1]} {row[2]} Course Name : {row[3]} E-mail : {row[4]} Enrollment Date : {row[5]} Grade : {grade}")
        except Error as e:
            print("Failed to retrieve Data : ",e)  


    def close_connection(self):
        if self.conn.is_connected():
            self.cursor.close()
            self.conn.close()
            print("SQL connection is closed")

def main():
    db = StudentDB()

    while True:
        print("\n Student Database Management System")
        print("1. Add student")
        print("2. View All student")
        print("3. Update Student")
        print("4. Delete Student")
        print("5. Search Student")
        print("6. Add Courses")
        print("7. View Courses")
        print("8. Add enrollment")
        print("9. view enrollment")
        print("10. View Courses for a Student")
        print("11. View Students in a Course")
        print("12. View Student and Course Details")
        print("13. Exit")

        choice = int(input("Enter your choices : "))

        if choice == 1:
            try:
                first_name = input("Enter your first name : ")
                if not db.isValidName(first_name):
                    raise ValueError("Enter the valid name.")
                last_name = input("Enter your last name : ")
                if not db.isValidName(last_name):
                    raise ValueError("Enter the valid name.")
                email = input("Enter the E-mail : ")
                if not db.isValidEmail(email):
                    raise ValueError("Enter the valid E-mail")
                major = input("Enter your major : ")
                if not db.isValidMajor(major):
                    raise ValueError("Enter the valid major")
                db.Add_student(first_name,last_name,email,major)
            except ValueError as v:
                print("Validation Failed! :",v)
        
        elif choice == 2:
            db.View_students()

        elif choice == 3:
            student_id = input("Enter student id to update : ")
            print("Which field you want to update : ")
            print("1. First name")
            print("2. Last Name")
            print("3. E mail")
            print("4. Major")
            field_choice = input("Enter your choice from 1-4 : ")
            fields = {'1':"first_name",'2':'last_name','3':'email','4':'major'}
            try:
                if not field_choice in fields:
                    raise ValueError("Invalid field Choice!")
                new_value = input(f"Enter the new {fields[field_choice]} : ")
                if field_choice == '1':
                    if not db.isValidName(new_value):
                        raise ValueError("Enter the valid name.")
                elif field_choice == '2':
                    if not db.isValidName(new_value):
                        raise ValueError("Enter the valid name.")
                elif field_choice == '3':
                    if not db.isValidEmail(new_value):
                        raise ValueError("Enter the valid E-mail")
                elif field_choice == '4':
                    if not db.isValidMajor(new_value):
                        raise ValueError("Enter the valid major")
                db.Update_students(student_id,fields[field_choice],new_value)
            except ValueError as v:
                print("Validation Failed :",v)
                
        elif choice == 4:
            student_id = input("Enter the student ID to delete : ")
            try:
                if not student_id.isnumeric():
                    raise ValueError("Enter the valid student_id")
                db.Delete_students(student_id)
            except ValueError as v:
                print("Validation Failed : ",v)

        elif choice == 5:
            search_term = input("Enter the search term : ")
            db.Search_students(search_term)

        elif choice == 6:
            try:
                course_code = input("Enter course code:")
                if not db.isValidAlphaNumeric(course_code):
                    raise ValueError("Enter the valid course code")
                course_name = input("Enter the course name : ")
                if not db.isValidMajor(course_name):
                    raise ValueError("Enter the valid course name")
                credits = int(input("Enter the credits :"))
                if not credits < 10:
                    raise ValueError("Enter the valid credits")
                instructor = input("Enter name of the instructor:")
                if not db.isValidName(instructor):
                    raise ValueError("Enter the valid name")
                db.Add_courses(course_code,course_name,credits,instructor)
            except ValueError as v:
                print("Validation Failed : ",v)

        elif choice == 7:
            db.View_Courses()

        elif choice == 8:
            try:
                student_id = int(input("Enter Student ID : "))
                student = str(student_id)
                if not db.isValidNumeric(student):
                    raise ValueError("Enter the Valid Student Id")
                course_id = int(input("Enter the Course ID : "))
                course = str(course_id)
                if not db.isValidNumeric(course):
                    raise ValueError("Enter the Valid course ID")
                enrollment_date = input("Enter the date in the format (YYYY-MM-DD) : ")
                if not db.isValidDate(enrollment_date):
                    raise ValueError("Enter the valid date")
                grade = input("Enter grade : ")
                if not db.isValidName(grade):
                    raise ValueError("Enter the valid grade")
                db.Add_enrollment(student_id,course_id,enrollment_date,grade)
            except ValueError as v:
                print("Validation Failed : ",v)
        elif choice == 9:
            db.View_enrollment()

        elif choice == 10:
            try:
                student_id = int(input("Enter the Student ID : "))
                student = str(student_id)
                if not db.isValidNumeric(student):
                    raise ValueError("Enter the valid student ID")
                db.get_student_courses(student_id)
            except ValueError as v:
                print("Validation Failed : ",v)

        elif choice == 11:
            try:
                course_id = int(input("Enter the Course ID : "))
                course = str(course_id)
                if not db.isValidNumeric(course):
                    raise ValueError("Enter the valid student ID")
                db.get_course_students(course_id)
            except ValueError as v:
                print("Validation Failed : ",v)

        elif choice == 12:
            try:
                student_id = int(input("Enter the Student ID : "))
                student = str(student_id)
                if not db.isValidNumeric(student):
                    raise ValueError("Enter the valid student ID")
                db.Student_and_Course_details(student_id)
            except ValueError as v:
                print("Validation Failed : ",v)

        elif choice == 13:
            db.close_connection()
            print("GoodBye")
            break

        else:
            print("Invalid Choice please try again..")

if __name__ == "__main__":
    main() 


