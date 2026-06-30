from flask import Flask, render_template, request, session, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "secret123"

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db = SQLAlchemy(app)


# User Table
class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(100))

    email = db.Column(db.String(100))

    password = db.Column(db.String(100))

class Task(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(100))

    assigned_to = db.Column(db.String(100))

    status = db.Column(db.String(50))


# Login Page
@app.route('/', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(
            email=email,
            password=password
        ).first()

        if user:

            session['user'] = user.email

            tasks = Task.query.all()

            return render_template(
                "dashboard.html",
                tasks=tasks
            )

        else:
            return "Invalid Email or Password"

    return render_template("login.html")
# Signup Page
@app.route('/signup', methods=['GET', 'POST'])
def signup():

    if request.method == 'POST':

        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Save user in database
        new_user = User(
            username=username,
            email=email,
            password=password
        )

        db.session.add(new_user)
        db.session.commit()

        return redirect('/')

    return render_template("signup.html")

@app.route('/create-task', methods=['GET', 'POST'])
def create_task():

    if request.method == 'POST':

        title = request.form['title']
        assigned_to = request.form['assigned_to']
        status = request.form['status']

        new_task = Task(
            title=title,
            assigned_to=assigned_to,
            status=status
        )

        db.session.add(new_task)
        db.session.commit()

        tasks = Task.query.all()
        return render_template(
    "dashboard.html",
    tasks=tasks
)

    return render_template("create_task.html")

@app.route('/update-task/<int:id>')
def update_task(id):

    task = Task.query.get(id)

    if task.status == "Pending":
        task.status = "Completed"

    else:
        task.status = "Pending"

    db.session.commit()

    tasks = Task.query.all()

    return render_template(
        "dashboard.html",
        tasks=tasks
    )

@app.route('/delete-task/<int:id>')
def delete_task(id):

    task = Task.query.get(id)

    db.session.delete(task)

    db.session.commit()

    tasks = Task.query.all()

    return render_template(
        "dashboard.html",
        tasks=tasks
    )

@app.route('/logout')
def logout():

    session.pop('user', None)

    return redirect('/')

# Create Database
with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run(debug=True)