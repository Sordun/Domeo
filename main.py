from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_pyfile("config.py")
SQLALCHEMY_DATABASE_URI = app.config["SQLALCHEMY_DATABASE_URI"]
SQLALCHEMY_TRACK_MODIFICATIONS = app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]

db = SQLAlchemy(app)


class Users(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=True)
    middle_name = db.Column(db.String(50), nullable=True)
    bornDate = db.Column(db.String(50), nullable=True)
    gender = db.Column(db.String(50), nullable=True)

    def __str__(self):
        return f"<users {self.name}>"


class Profiles(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    education = db.Column(db.String(50), nullable=True)
    comment = db.Column(db.Text(500), nullable=True)
    citizenship = db.Column(db.String(50), nullable=True)

    id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

    def __str__(self):
        return f"<profiles {self.user_id}>"


@app.route('/', methods=("POST", "GET"))
def index():
    if request.method == "POST":
        try:
            u = Users(name=request.form['userName'], middle_name=request.form['userSurname'],
                      bornDate=request.form['dateBorn'], gender=request.form['gender'])
            db.session.add(u)
            db.session.flush()

            p = Profiles(education=request.form['education'], comment=request.form['comment'],
                         citizenship=request.form['citizen'], id=u.user_id)
            db.session.add(p)
            db.session.commit()
        except:
            db.session.rollback()
            print("Ошибка добавления в БД")

    return render_template("picture.html")


if __name__ == '__main__':
    app.run(debug=True)
