
Student Database Management System

A simple Python + MySQL project where I’m building a mini student management system from scratch.
This project is my way of learning Python, SQL, and database design by actually coding instead of just reading tutorials.

Features (so far):

1. Add new students (with input validation)

2. View all students

3. Update student details (currently debugging field validation)

4. Search students by name, email, or major (still tweaking validation & query)

5. Delete student records (basic version done)

Database Structure:

# students : stores student info

# courses : stores course info

# enrollment : many-to-many relationship between students & courses

What I’m Working On Next:

Fixing bugs in update & search functions

Adding proper JOIN queries for course and enrollments

Making validation more robust (e.g. regex checks, date formatting)

Writing cleaner error handling

Why I Built This : 

I wanted to push myself beyond tutorials and actually struggle through building a project.
Yes, there are bugs. But that’s the point — this repo shows my process, not just the final result.

Built-in Modules Used :

re → for regex validation

datetime → for handling dates
