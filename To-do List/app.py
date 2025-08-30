from flask import Flask,request,render_template,redirect,url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://devuser:Shivam%40123@localhost/todoapp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    content = db.Column(db.String(100), nullable = False)
    completed = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Task {self.id}:{self.content}>'
    
with app.app_context():
        db.create_all()
    

@app.route('/')
def home():
    tasks = Task.query.all()
    return render_template("index.html",tasks = tasks)
        

@app.route('/add')
def add_task():
    return render_template("add_task.html")

@app.route('/edit/<int:task_id>')
def edit_task(task_id):
    return render_template('edit.html',task_id=task_id)

@app.route('/add_task',methods = ['POST'])
def add():
    task = request.form['task']
    new_task = Task(content=task)
    db.session.add(new_task)
    db.session.commit()
    return render_template('add.html',task=task)
    
@app.route('/delete/<int:task_id>')
def delete(task_id):
    tasks = Task.query.get(task_id)
    if tasks:
        db.session.delete(tasks)
        db.session.commit()
        return render_template('delete.html', task= tasks.content)
    
@app.route('/update/<int:task_id>', methods = ['POST'])
def update(task_id):
    new_content = request.form['task']
    task = Task.query.get(task_id)
    if task:
        task.content = new_content
        db.session.commit()
        return render_template('update.html')

@app.route('/completed/<int:task_id>' ,methods=['POST']) 
def completed(task_id):
    task = Task.query.get(task_id)
    if task:
        task.completed = not task.completed
        db.session.commit()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)



