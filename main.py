from flask import Flask, render_template, redirect
from data import db_session
from data.users import User
from data.jobs import Jobs
import datetime
from forms.register import RegisterForm


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init("db/mars.db")
    app.run(port=5000, host='127.0.0.1')


@app.route("/")
def index():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs)
    return render_template("index.html", jobs=jobs)


@app.route('/register',  methods=['GET', 'POST'])
def add_user():
    password = False
    email = False
    form = RegisterForm()
    if form.hashed_password.data != form.confirm_password.data:
        password = True
    db_sess = db_session.create_session()
    emails = []
    for user in db_sess.query(User).all():
        emails.append(user.email)
    if form.email.data in emails:
        email = True
    if form.validate_on_submit() and not password and not email:
        user = User()
        user.surname = form.surname.data
        user.name = form.name.data
        user.age = form.age.data
        user.position = form.position.data
        user.speciality = form.speciality.data
        user.address = form.address.data
        user.email = form.email.data
        user.set_password(form.hashed_password.data)
        db_sess.add(user)

        db_sess.commit()
        login_user(user)
        return redirect('/')
    return render_template('register.html', title='Регистрация',
                           password=password, email=email, form=form)


if __name__ == '__main__':
    main()
