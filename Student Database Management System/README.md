# Student Database Management System

A simple Python + MySQL project to manage student records. Supports input validation, error handling, and relational queries across multiple tables.

# Features

- Add Students – with validation for name, email, date, etc.

- View Students – list all student records.

- Update Student Info – update name, email, or major safely.

- Delete Student – remove a student by ID.

- Search Students – search by name, email, or major (with validation).

- Relational Tables – includes students, courses, and enrollments.

- Error Handling – clean messages instead of crashes.

# Database Schema

- students

student_id (PK)

first_name

last_name

email

major

- courses

course_id (PK)

course_name

credits

- enrollment (Many-to-Many)

enrollment_id (PK)

student_id (FK → students)

course_id (FK → courses)

enrollment_date

grade
