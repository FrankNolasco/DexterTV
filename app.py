from flask import Flask
from datetime import date
import decimal
import flask.json
from flask.templating import render_template
from config import DB_URL
from flask_sqlalchemy import SQLAlchemy
class MyJSONEncoder(flask.json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, date):
            return obj.isoformat()
        if isinstance(obj, decimal.Decimal):
            return str(obj)
        return super(MyJSONEncoder, self).default(obj)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DB_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class IModel(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer , primary_key = True)

    def create(self):
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except:
            return False

    def update(self, updates):
        pass

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except:
            return False

class Categoria(IModel):
    __tablename__ = 'categoria'
    nombre = db.Column(db.String(200), nullable=False)

class Deporte(IModel):
    __tablename__ = "deporte"
    nombre = db.Column(db.String(200), nullable=False)
    portada_url = db.Column(db.Text, nullable=False)
    descripcion =  db.Column(db.Text, nullable=True)
    fecha_hora = db.Column(db.DateTime, nullable=False)
    esRepeticion = db.Column(db.Boolean, nullable=False)
    video = db.Column(db.Text, nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey("categoria.id"), nullable = False)

class Pelicula(IModel):
    __tablename__ = "pelicula"
    nombre = db.Column(db.String(200), nullable=False)
    portada_url = db.Column(db.Text, nullable=False)
    descripcion =  db.Column(db.Text, nullable=True)
    fecha_hora = db.Column(db.DateTime, nullable=False)
    duracion = db.Column(db.String(50), nullable=False)
    video = db.Column(db.Text, nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey("categoria.id"), nullable = False)

class Serie(IModel):
    __tablename__ = "serie"
    nombre = db.Column(db.String(200), nullable=False)
    portada_url = db.Column(db.Text, nullable=False)
    descripcion =  db.Column(db.Text, nullable=True)
    trailer = db.Column(db.Text, nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey("categoria.id"), nullable = False)

class Temporada(IModel):
    __tablename__ = "temporada"
    nombre = db.Column(db.String(200), nullable=False)
    descripcion =  db.Column(db.Text, nullable=True)
    trailer = db.Column(db.Text, nullable=False)
    serie_id = db.Column(db.Integer, db.ForeignKey("serie.id"), nullable = False)

class Episodio(IModel):
    __tablename__ = "episodio"
    nombre = db.Column(db.String(200), nullable=False)
    portada_url = db.Column(db.Text, nullable=False)
    descripcion =  db.Column(db.Text, nullable=True)
    duracion = db.Column(db.String(50), nullable=False)
    video = db.Column(db.Text, nullable=False)
    temporada_id = db.Column(db.Integer, db.ForeignKey("temporada.id"), nullable = False)

class Usuario(IModel):
    __tablename__ = "usuario"
    nombres = db.Column(db.String(200), nullable=False)
    perfil_url = db.Column(db.Text, nullable=False)
    username =  db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    rol_id =  db.Column(db.Integer, db.ForeignKey("rol.id"), nullable = False)

class Rol(IModel):
    __tablename__ = "rol"
    nombre = db.Column(db.String(200), nullable=False)

with app.app_context():
    db.create_all()

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET"])
def login():
    return render_template("login.html")

@app.route("/user/deportes", methods=["GET"])
def user_deportes():
    deportes = db.session.query(Deporte).all()
    return render_template("user/deportes.html", deportes = deportes)

@app.route("/user/deporte/<int:id>", methods=["GET"])
def user_deporte(id):
    deporte = Deporte.query.get(id)
    return render_template("user/deporte.html", deporte = deporte)

@app.route("/user/peliculas", methods=["GET"])
def user_peliculas():
    peliculas = db.session.query(Pelicula).all()
    return render_template("user/peliculas.html", peliculas = peliculas)

@app.route("/user/pelicula/<int:id>", methods=["GET"])
def user_pelicula(id):
    pelicula = Pelicula.query.get(id)
    return render_template("user/pelicula.html", pelicula = pelicula)

@app.route("/user/perfil", methods=["GET"])
def user_perfil():
    return render_template("user/perfil.html")

@app.route("/user/series", methods=["GET"])
def user_series():
    series = db.session.query(Serie).all()
    return render_template("user/series.html", series = series)

@app.route("/user/serie/<int:id>", methods=["GET"])
def user_serie(id):
    serie = Serie.query.get(id)
    return render_template("user/serie.html", serie = serie)


if __name__ == '__main__':
    app.run()