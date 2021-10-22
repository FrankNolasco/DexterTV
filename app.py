from os import error
from flask import Flask, request
from datetime import date
import decimal
import flask.json
import json
from flask.templating import render_template
from sqlalchemy.orm import session
from config import DB_URL
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.utils import redirect
class MyJSONEncoder(flask.json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, date):
            return obj.isoformat()
        if isinstance(obj, decimal.Decimal):
            return str(obj)
        return super(MyJSONEncoder, self).default(obj)

app = Flask(__name__)
cors = CORS(app)
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
    return redirect("/login")

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

@app.route("/user/series", methods=["GET"])
def user_series():
    series = db.session.query(Serie).all()
    return render_template("user/series.html", series = series)

@app.route("/user/serie/<int:id>", methods=["GET"])
def user_serie(id):
    serie = Serie.query.get(id)
    return render_template("user/serie.html", serie = serie)


@app.route("/user/temporadas/<int:id>", methods=["GET"])
def user_temp_serie(id):
    temporadas = db.session.query(Temporada).filter_by(serie_id = id).all()
    return render_template('user/temporadas.html', temporadas = temporadas)

@app.route("/user/capitulos/<int:id>", methods=["GET"])
def user_capitulo_serie(id):
    capitulos = db.session.query(Episodio).filter_by(temporada_id = id).all()
    return render_template('user/capitulos.html', capitulos = capitulos)

#Administracion routes
@app.route("/log-in/validate", methods=["POST"])
def login_validate_user():
    username = request.form["username"]
    password = request.form["password"]
    UsuarioBD = Usuario.query.filter_by(username=username, password = password).first()
    print(UsuarioBD)
    if(UsuarioBD):
        if(UsuarioBD.rol_id == 1):
            return redirect('/admin/peliculas')
        else:
            return redirect('/user/peliculas')
    else:
        return redirect('/login')

#USUARIO
@app.route("/admin/usuarios", methods=["GET"])
def admin_usuario():
    roles = db.session.query(Rol).all()
    return render_template("administrador/usuarios.html", roles= roles)

@app.route("/admin/buscar/usuarios/<int:id>", methods=["GET"])
def buscar_usuario(id):
    usuario = Usuario.query.get(id)
    if(usuario):
        return flask.json.jsonify(
            {
                'not_found': 0,
                'id':usuario.id, 
                'nombres': usuario.nombres,
                'perfil_url': usuario.perfil_url,
                'username': usuario.username,
                'password': usuario.password,
                'rol_id': usuario.rol_id
            }
        )
    else :
        return flask.json.jsonify({ 'not_found': 1 })

@app.route("/admin/usuarios/registrar", methods=["POST"])
def registrar_usuarios():
    nombres = request.form["nombres"]
    username = request.form["username"]
    password = request.form["password"]
    perfil_url = request.form["perfil_url"]
    rol_id = request.form["rol_id"]
    try:
        UsuarioBD = Usuario(nombres=nombres,
        username = username, password = password, perfil_url= perfil_url,
        rol_id=rol_id)
        db.session.add(UsuarioBD)
        db.session.commit()
        return redirect("/admin/usuarios")
    except Exception as e:
        print(e)
        return redirect("/admin/usuarios")

@app.route("/admin/usuarios/modificar", methods=["POST"])
def modificar_usuarios():
    id = request.form["id"]
    print(id)
    try:
        UsuarioBD = Usuario.query.filter_by(id=id).first()
        UsuarioBD.nombres = request.form["nombres"]
        UsuarioBD.username = request.form["username"]
        UsuarioBD.password = request.form["password"]
        UsuarioBD.perfil_url = request.form["perfil_url"]
        UsuarioBD.rol_id = request.form["rol_id"]
        db.session.commit()
        return redirect("/admin/usuarios")
    except Exception as e:
        print(e)
        return redirect("/admin/usuarios")


#CATEGORIAS
@app.route("/admin/categorias", methods=["GET"])
def admin_categoria():
    return render_template("administrador/categorias.html")

@app.route("/admin/buscar/categorias/<int:id>", methods=["GET"])
def buscar_categorias(id):
    categoria = Categoria.query.get(id)
    if(categoria):
        return flask.json.jsonify(
            {
                'not_found': 0,
                'id':categoria.id, 
                'nombre': categoria.nombre,
            }
        )
    else :
        return flask.json.jsonify({ 'not_found': 1 })

@app.route("/admin/categorias/registrar", methods=["POST"])
def registrar_categorias():
    nombre = request.form["nombre"]
    try:
        CategoriaBD = Categoria(nombre=nombre)
        db.session.add(CategoriaBD)
        db.session.commit()
        return redirect("/admin/categorias")
    except Exception as e:
        print(e)
        return redirect("/admin/categorias")

@app.route("/admin/categorias/modificar", methods=["POST"])
def modificar_categorias():
    id = request.form["id"]
    print(id)
    try:
        CategoriaBD = Categoria.query.filter_by(id=id).first()
        CategoriaBD.nombre = request.form["nombre"]
        db.session.commit()
        return redirect("/admin/categorias")
    except Exception as e:
        print(e)
        return redirect("/admin/categorias")



#PELICULAS
@app.route("/admin/peliculas", methods=["GET"])
def admin_peliculas():
    categorias = db.session.query(Categoria).all()
    return render_template("administrador/peliculas.html", typeForms = 'PELICULA', categorias = categorias)


@app.route("/admin/buscar/peliculas/<int:id>", methods=["GET"])
def buscar_peliculas(id):
    peliculas = Pelicula.query.get(id)
    if(peliculas):
        return flask.json.jsonify(
            {
                'not_found': 0,
                'id':peliculas.id, 
                'nombre': peliculas.nombre,
                'portada_url': peliculas.portada_url,
                'descripcion': peliculas.descripcion,
                'fecha_hora': date.isoformat(peliculas.fecha_hora),
                'duracion': peliculas.duracion,
                'video': peliculas.video,
                'categoria_id': peliculas.categoria_id
            }
        )
    else :
        return flask.json.jsonify({ 'not_found': 1 })

@app.route("/admin/peliculas/registrar", methods=["POST"])
def registrar_peliculas():
    nombre = request.form["nombre"]
    descripcion = request.form["descripcion"]
    portada_url = request.form["portada_url"]
    fecha_hora = request.form["fecha_hora"]
    duracion = request.form["duracion"]
    video = request.form["video"]
    categoria_id = request.form["categoria_id"]
    try:
        peliculaBD = Pelicula(nombre=nombre, descripcion=descripcion,
        portada_url = portada_url, fecha_hora = fecha_hora, 
        duracion = duracion, video = video, categoria_id = categoria_id)
        db.session.add(peliculaBD)
        db.session.commit()
        return redirect("/admin/peliculas")
    except Exception as e:
        print(e)
        return redirect("/admin/peliculas")

@app.route("/admin/peliculas/modificar", methods=["POST"])
def modificar_peliculas():
    id = request.form["id"]
    print(id)
    try:
        peliculaBD = Pelicula.query.filter_by(id=id).first()
        peliculaBD.nombre = request.form["nombre"]
        peliculaBD.descripcion = request.form["descripcion"]
        peliculaBD.portada_url = request.form["portada_url"]
        peliculaBD.fecha_hora = request.form["fecha_hora"]
        peliculaBD.duracion = request.form["duracion"]
        peliculaBD.video = request.form["video"]
        peliculaBD.categoria_id = request.form["categoria_id"]
        db.session.commit()
        return redirect("/admin/peliculas")
    except Exception as e:
        print(e)
        return redirect("/admin/peliculas")

#SERIES
@app.route("/admin/series", methods=["GET"])
def admin_serie():
    categorias = db.session.query(Categoria).all()
    return render_template("administrador/series.html", categorias = categorias)

@app.route("/admin/buscar/series/<int:id>", methods=["GET"])
def buscar_series(id):
    serie = Serie.query.get(id)
    if(serie):
        return flask.json.jsonify(
            {
                'not_found': 0,
                'id':serie.id, 
                'nombre': serie.nombre,
                'portada_url': serie.portada_url,
                'descripcion': serie.descripcion,
                'trailer': serie.trailer,
                'categoria_id': serie.categoria_id
            }
        )
    else :
        return flask.json.jsonify({ 'not_found': 1 })

@app.route("/admin/series/registrar", methods=["POST"])
def registrar_serie():
    nombre = request.form["nombre"]
    descripcion = request.form["descripcion"]
    portada_url = request.form["portada_url"]
    trailer = request.form["trailer"]
    categoria_id = request.form["categoria_id"]
    try:
        SerieBD = Serie(nombre=nombre, descripcion=descripcion,
        portada_url = portada_url, trailer = trailer,
         categoria_id = categoria_id)
        db.session.add(SerieBD)
        db.session.commit()
        return redirect("/admin/series")
    except Exception as e:
        print(e)
        return redirect("/admin/series")

@app.route("/admin/series/modificar", methods=["POST"])
def modificar_series():
    id = request.form["id"]
    print(id)
    try:
        SerieBD = Serie.query.filter_by(id=id).first()
        SerieBD.nombre = request.form["nombre"]
        SerieBD.descripcion = request.form["descripcion"]
        SerieBD.portada_url = request.form["portada_url"]
        SerieBD.trailer = request.form["trailer"]
        SerieBD.categoria_id = request.form["categoria_id"]
        db.session.commit()
        return redirect("/admin/series")
    except Exception as e:
        print(e)
        return redirect("/admin/series")


#TEMPORADAS
@app.route("/admin/temporadas/<int:id_serie>", methods=["GET"])
def admin_temporadas(id_serie):
    return render_template("administrador/temporadas.html", id = id_serie)



@app.route("/admin/buscar/temporada/<int:id>", methods=["GET"])
def buscar_temporada(id):
    temporadas = db.session.query(Temporada).filter_by(serie_id = id).all()
    if(temporadas):
        data = []
        for temporada in temporadas:
            data.append({
                'id':temporada.id, 
                'nombre': temporada.nombre,
                'descripcion': temporada.descripcion,
                'trailer': temporada.trailer,
                'serie_id': temporada.serie_id
            })
        print(data)
        return flask.json.jsonify(
            {
                'not_found': 0,
                'data': json.dumps(data)
            }
        )
    else :
        return flask.json.jsonify({ 'not_found': 1 })

@app.route("/admin/temporadas/registrar", methods=["POST"])
def registrar_temporada():
    print(request.form)
    nombre = request.form["nombre"]
    descripcion = request.form["descripcion"]
    trailer = request.form["trailer"]
    serie_id = request.form["serie_id"]
    try:
        TemporadaBD = Temporada(nombre=nombre, descripcion=descripcion, 
        trailer = trailer, serie_id = serie_id)
        db.session.add(TemporadaBD)
        db.session.commit()
        return redirect("/admin/temporadas/"+serie_id)
    except Exception as e:
        print(e)
        return redirect("/admin/temporadas"+serie_id)

@app.route("/admin/temporadas/modificar", methods=["POST"])
def modificar_temporada():
    id = request.form["id"]
    serie_id = request.form["serie_id"]
    try:
        SerieBD = Temporada.query.filter_by(id=id).first()
        SerieBD.nombre = request.form["nombre"]
        SerieBD.descripcion = request.form["descripcion"]
        SerieBD.trailer = request.form["trailer"]
        db.session.commit()
        return redirect("/admin/temporadas/"+serie_id)

    except Exception as e:
        print(e)
        return redirect("/admin/temporadas/"+serie_id)

#EPISODIOS
@app.route("/admin/episodios/<int:id>", methods=["GET"])
def admin_episodios(id):
    return render_template("administrador/episodio.html", id = id)


@app.route("/admin/buscar/episodios/<int:id_temporada>", methods=["GET"])
def buscar_episodio(id_temporada):
    episodios = db.session.query(Episodio).filter_by(temporada_id = id_temporada).all()
    if(episodios):
        data = []
        for episodio in episodios:
            data.append({
                'id':episodio.id, 
                'nombre': episodio.nombre,
                'portada_url': episodio.portada_url,
                'descripcion': episodio.descripcion,
                'duracion': episodio.duracion,
                'video': episodio.video,
                'temporada_id': episodio.temporada_id
            })
        print(data)
        return flask.json.jsonify(
            {
                'not_found': 0,
                'data': json.dumps(data)
            }
        )
    else :
        return flask.json.jsonify({ 'not_found': 1 })

@app.route("/admin/episodios/registrar", methods=["POST"])
def registrar_episodio():
    nombre = request.form["nombre"]
    descripcion = request.form["descripcion"]
    duracion = request.form["duracion"]
    video = request.form["video"]
    temporada_id = request.form["temporada_id"]
    portada_url = request.form["portada_url"]
    try:
        EpisodioBD = Episodio(nombre=nombre, portada_url = portada_url, descripcion=descripcion,duracion=duracion,video = video, temporada_id = temporada_id)
        db.session.add(EpisodioBD)
        db.session.commit()
        return redirect("/admin/episodios/" + temporada_id)
    except Exception as e:
        print(e)
        return redirect("/admin/episodios/" + temporada_id)

@app.route("/admin/episodios/modificar", methods=["POST"])
def modificar_episodio():
    id = request.form["id"]
    temporada_id = request.form["temporada_id"]
    print(id)
    try:
        EpisodioBD = Episodio.query.filter_by(id=id).first()
        EpisodioBD.nombre = request.form["nombre"]
        EpisodioBD.portada_url = request.form["portada_url"]
        EpisodioBD.descripcion = request.form["descripcion"]
        EpisodioBD.duracion = request.form["duracion"]
        EpisodioBD.video = request.form["video"]
        db.session.commit()
        return redirect("/admin/episodios/" + temporada_id)
    except Exception as e:
        print(e)
        return redirect("/admin/episodios/" + temporada_id)


#Deportes
@app.route("/admin/deportes", methods=["GET"])
def admin_deportes():
    categorias = db.session.query(Categoria).all()
    return render_template("administrador/deportes.html", categorias = categorias)

@app.route("/admin/buscar/deportes/<int:id>", methods=["GET"])
def buscar_deportes(id):
    deporte = Deporte.query.get(id)
    if(deporte):
        return flask.json.jsonify(
            {
                'not_found': 0,
                'id':deporte.id, 
                'nombre': deporte.nombre,
                'portada_url': deporte.portada_url,
                'descripcion': deporte.descripcion,
                'fecha_hora': date.isoformat(deporte.fecha_hora),
                'esRepeticion': deporte.esRepeticion,
                'video': deporte.video,
                'categoria_id': deporte.categoria_id
            }
        )
    else :
        return flask.json.jsonify({ 'not_found': 1 })

@app.route("/admin/deportes/registrar", methods=["POST"])
def registrar_deportes():
    nombre = request.form["nombre"]
    descripcion = request.form["descripcion"]
    portada_url = request.form["portada_url"]
    fecha_hora = request.form["fecha_hora"]
    esRepeticion = False
    video = request.form["video"]
    categoria_id = request.form["categoria_id"]
    try:
        DeportesDB = Deporte(nombre=nombre, descripcion=descripcion,
        portada_url = portada_url, fecha_hora = fecha_hora, 
        esRepeticion = esRepeticion, video = video, categoria_id = categoria_id)
        db.session.add(DeportesDB)
        db.session.commit()
        return redirect("/admin/deportes")
    except Exception as e:
        print(e)
        return redirect("/admin/deportes")

@app.route("/admin/deportes/modificar", methods=["POST"])
def modificar_deportes():
    id = request.form["id"]
    print(id)
    try:
        DeporteBD = Serie.query.filter_by(id=id).first()
        DeporteBD.nombre = request.form["nombre"]
        DeporteBD.descripcion = request.form["descripcion"]
        DeporteBD.portada_url = request.form["portada_url"]
        DeporteBD.fecha_hora = request.form["fecha_hora"]
        DeporteBD.esRepeticion = request.form["esRepeticion"]
        DeporteBD.video = request.form["video"]
        DeporteBD.categoria_id = request.form["categoria_id"]
        db.session.commit()
        return redirect("/admin/deportes")
    except Exception as e:
        print(e)
        return redirect("/admin/deportes")


if __name__ == '__main__':
    app.run()