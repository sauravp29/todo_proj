from curses import flash
from fileinput import filename
from flask import Flask, render_template, request, redirect, url_for 
from flask_sqlalchemy import SQLAlchemy
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads/'
# app.secret_key = b'_5#y2L"F4Q8z\n\xec]iasdfffsd/'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
  return '.' in filename and \
  filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



# /// = relative path, //// = absolute path
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

with app.app_context():
    db.create_all()
@app.before_first_request
def create_tables():
    db.create_all()

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)
    


@app.route("/", methods=['GET'])
def home():
    todo_list = Todo.query.all()
    return render_template("base.html", todo_list=todo_list)
    

@app.route("/add", methods=["GET","POST"])
def add():
    if request.method == "POST":
        title = request.form.get("title")
        file = request.files.get("file")
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # file.save(secure_filename(file.filename))
        # file.save(os.path.join(app.config['UPLOAD_FOLDER']))
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    new_todo = Todo(title=title, complete=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("home", name=file.filename)) 

@app.route("/update/<int:todo_id>")
def update(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("home"))

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
    app.config['SESSION_TYPE'] = 'filesystem'

