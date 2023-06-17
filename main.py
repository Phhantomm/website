from flask import Flask, redirect, url_for, render_template, request, session, flash
from flask_sqlalchemy import SQLAlchemy
# import os
# os.system("pip install Flask-SQLAlchemy")

app = Flask(__name__)
app.config['SECRET_KEY'] = 'pythonwork'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.sqlite'
db = SQLAlchemy(app)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(80), nullable=False)
    author = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float, nullable=False)

    def __str__(self):
        return f'სათაური -  {self.title}, ავტორი - {self.author}, ფასი - {self.price}'


with app.app_context():
    db.create_all()
    # b1 = Book(title='Across the spiderverse', author='galaktion tabidze', price=100)
    # db.session.add(b1)
    # db.session.commit()
    # b7 = Book.query.first()
    # print(b7)
    # all = Book.query.all()
    # b6 = Book.query.get(5)
    # db.session.delete(b6)
    # db.session.commit()
    # idk = Book.query.filter_by(author='ilia chavchavadze').all()
    # for each in all:
    #     print(each)


@app.route('/')
def home():
    all_books = Book.query.all()
    return render_template('index.html', all_books=all_books)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        session['username'] = username
        return redirect(url_for('user'))

    return render_template('login.html')



@app.route('/user')
def user():
    subjects = ['Python', 'Calculus', 'DB']
    return render_template('user.html',  subjects=subjects)


@app.route('/<name>/<age>')
def userage(name, age):
    return f'Hello {name}, your age is {age}'

@app.route('/logout')
def logout():
    session.pop('username', None)
    return 'you are logged out'


@app.route('/books', methods=['GET', 'POST'])
def books():
    if request.method == 'POST':
        t = request.form['title']
        a = request.form['author']
        p = request.form['price']
        if t == '' or a == '' or p == '':
            flash('u missed few lines', 'error')
        elif not p.isdecimal():
            flash('price cant be words dumbass')
        else:
            b1 = Book(title=t, author=a, price=float(p))
            db.session.add(b1)
            db.session.commit()
            flash('book was added', 'info')
    return render_template('books.html')


if __name__ == "__main__":
    app.run(debug=True)