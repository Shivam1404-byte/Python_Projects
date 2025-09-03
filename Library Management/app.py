from flask import Flask,request,render_template,url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime,timedelta

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://devuser:Shivam%40123@localhost/Library'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#Student Table
class Student(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    age = db.Column(db.Integer,nullable = False)

# Books Table
class Book(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    title = db.Column(db.String(100), nullable = False)
    author = db.Column(db.String(100), nullable = False)
    available = db.Column(db.Boolean, default = True)

class Issued(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'),nullable = False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'),nullable = False)
    issue_date = db.Column(db.DateTime, default=datetime.now())
    return_date = db.Column(db.DateTime, nullable = False)
    returned = db.Column(db.Boolean, default=False)

    student = db.relationship('Student',backref = db.backref('issues',lazy=True))
    book = db.relationship('Book',backref=db.backref('issues'),lazy=True)

with app.app_context():
    db.create_all()

# Home Page
@app.route("/")
def home():
    return render_template('home.html')

# Take input to add member to the database
@app.route("/Add_member")
def Add_member():
    return render_template('Add_member.html')

# Add the data to the database
@app.route("/Add", methods=['POST'])
def Add():
    name = request.form['name']
    age = request.form['age']
    new_member = Student(name=name,age=age)
    db.session.add(new_member)
    db.session.commit()
    return render_template('Add.html')

# View data of members
@app.route("/view")
def view():
    members = Student.query.all()
    return render_template('view_member.html',members=members)

# Open form to Add the books
@app.route("/Add_books")
def Add_books():
    return render_template('Add_books.html')

# Add the data of books in database
@app.route("/AddBook",methods=['POST'])
def AddBook():
    title = request.form['book']
    author = request.form['author']
    new_book = Book(title = title,author=author)
    db.session.add(new_book)
    db.session.commit()
    return render_template('AddBook.html')

# View books stored in the database
@app.route("/View_Books")
def View_books():
    books = Book.query.all()
    return render_template('View_books.html',books=books)

# Open form to issue the book
@app.route("/issue_book")
def issue_book():
    student = Student.query.all()
    books = Book.query.all()
    return render_template("Issuebook.html",students=student,books=books)

# Store the data of the issued book and update the availability of book on Book table
@app.route("/Issue",methods=['POST'])
def Issue():
    student_id = request.form['student_id']
    book_id = request.form['book_id']
    returnDateInput = request.form['datetime']
    book = Book.query.get(book_id)
    if not book:
        return "<h1> Book not found</h1>"
    if not book.available:
        return "<h1>Book is already issued </h1>"

    if returnDateInput: 
        return_date = datetime.strptime(returnDateInput,"%Y-%m-%d")
    else:
        return_date = datetime.now() + timedelta(days=7)
    
    IssuedBook = Issued(student_id=student_id,book_id=book_id,return_date=return_date)
    db.session.add(IssuedBook)
    book.available = False
    db.session.commit()
    return f"""<h1>Book {book.title} issued successfully
        <a href="{{url_for('home')}}" style="padding:6px;background-color: blue;color:white;text-decoration: none;font-weight: bold;">Back to home</a>
    """

# View the data of the issued books
@app.route("/view_Issued")
def view_Issued():
    Issue_books = Issued.query.all()
    return render_template('view_Issued.html',Issue_books=Issue_books)

# To open the form to return the book
@app.route('/return_book')
def return_book():
    books = Book.query.all()
    return render_template("return_book.html", books=books)

# store the value in databse
@app.route('/Return',methods=['POST'])
def Return():
    book_id = request.form['book_id']
    book = Book.query.get(book_id)
    Issued_record = Issued.query.filter_by(book_id=book_id, returned = False).first()
    if book and Issued_record:
        Issued_record.return_date = datetime.now()
        Issued_record.returned = True
        book.available = True
        db.session.commit()
        return f"<h1>Book {book.title} returned Successfully</h1>"
    return """<h1>Book not found</h1>
            <a href="{{url_for('home')}}" style="padding:6px;background-color: blue;color:white;text-decoration: none;font-weight: bold;">Back to home</a>
    """

