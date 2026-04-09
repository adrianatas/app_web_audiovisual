from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)

app.config["SECRET_KEY"] = "clave_super_secreta"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# -------------------- MODELOS --------------------

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(10), default="cliente")  # cliente o admin

class Content(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100))
    tipo = db.Column(db.String(10))  # pelicula o series
    categoria = db.Column(db.String(50))
    duracion = db.Column(db.Integer)  # minutos
    temporadas = db.Column(db.Integer, nullable=True)
    capitulos = db.Column(db.Integer, nullable=True)
    duracion_capitulo = db.Column(db.Integer, nullable=True)
    imagen = db.Column(db.String(200))  # ruta relativa a static/

class UserContent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    content_id = db.Column(db.Integer, db.ForeignKey('content.id'))
    favorito = db.Column(db.Boolean, default=False)
    visto = db.Column(db.Boolean, default=False)
    content = db.relationship('Content')

# -------------------- LOGIN --------------------

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# -------------------- FUNCIONES --------------------

def crear_admin():
    admin = User.query.filter_by(username="admin").first()
    if not admin:
        nuevo_admin = User(username="admin", password="admin123", role="admin")
        db.session.add(nuevo_admin)
        db.session.commit()
        print("✅ Usuario admin creado")
    else:
        print("ℹ️ El admin ya existe")

def crear_contenidos_prueba():
    if not Content.query.first():
        peli1 = Content(
            titulo="Matrix",
            tipo="pelicula",
            categoria="Ciencia ficción",
            duracion=136,
            imagen="images/pelicula1.jpg"
        )
        serie1 = Content(
            titulo="The Chosen",
            tipo="series",
            categoria="Drama Cristiana",
            temporadas=6,
            capitulos=24,
            duracion_capitulo=50,
            imagen="images/serie1.jpg"
        )
        #Pelicula nueva
        peli2 = Content(
            titulo="Avatar: Fuego y Ceniza",
            tipo="pelicula",
            categoria="Ciencia ficción",
            duracion=190,
            imagen="images/pelicula2.jpg"
        )
        # Nueva serie
        serie2 = Content(
            titulo="Game Of Thrones",
            tipo="series",
            categoria="Fantasía medieval",
            temporadas=8,
            capitulos=73,
            duracion_capitulo=60,
            imagen="images/serie2.jpg"
        )
        # Otra peli
        peli3 = Content(
            titulo="Como entrenar a tu Dragón",
            tipo="pelicula",
            categoria="Ciencia ficción",
            duracion=125,
            imagen="images/pelicula3.jpg"
        )
        # Otra serie
        serie3 = Content(
            titulo="The Witcher",
            tipo="series",
            categoria="Drama",
            temporadas=4,
            capitulos=32,
            duracion_capitulo=50,
            imagen="images/serie3.jpg"
        )
        peli4 = Content(
            titulo="Anastasia",
            tipo="pelicula",
            categoria="Animación. Drama. Musical. Infantil | Revolución Rusa",
            duracion=100,
            imagen="images/pelicula4.jpg"
        )
        serie4 = Content(
            titulo="The Originals",
            tipo="series",
            categoria="Drama | Ciencia Ficción",
            temporadas=5,
            capitulos=92,
            duracion_capitulo=50,
            imagen="images/serie4.jpg"
        )
        db.session.add_all([peli1, peli2, peli3, peli4, serie1, serie2, serie3, serie4])
        db.session.commit()
        print("✅ Contenido de prueba creado")
    else:
        print("ℹ️ Ya existe contenido de prueba")

# -------------------- RUTAS --------------------

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if User.query.filter_by(username=username).first():
            return render_template("register.html", error="El usuario ya existe")
        new_user = User(username=username, password=password, role="cliente")
        db.session.add(new_user)
        db.session.commit()
        return redirect("/login")
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            login_user(user)
            if user.role == "admin":
                return redirect("/admin")
            else:
                return redirect("/catalogo")
        return render_template("login.html", error="Usuario o contraseña incorrectos")
    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/login")

# -------------------- ADMIN --------------------

@app.route("/admin")
@login_required
def admin():
    # Solo permitir acceso si el usuario es admin
    if current_user.role != "admin":
        return redirect("/catalogo")

    usuarios = User.query.all()
    contenidos = Content.query.all()

    return render_template("admin.html", usuarios=usuarios, contenidos=contenidos)

# -------------------- CATÁLOGO --------------------

@app.route("/catalogo")
@login_required
def catalogo():
    peliculas = Content.query.filter_by(tipo="pelicula").all()
    series = Content.query.filter_by(tipo="series").all()
    return render_template("catalogo.html", peliculas=peliculas, series=series)

# -------------------- FAVORITOS / VISTOS --------------------

@app.route("/favorito/<int:content_id>")
@login_required
def favorito(content_id):
    registro = UserContent.query.filter_by(user_id=current_user.id, content_id=content_id).first()
    if not registro:
        registro = UserContent(user_id=current_user.id, content_id=content_id)
    registro.favorito = True
    db.session.add(registro)
    db.session.commit()
    return redirect("/catalogo")

@app.route("/visto/<int:content_id>")
@login_required
def visto(content_id):
    registro = UserContent.query.filter_by(user_id=current_user.id, content_id=content_id).first()
    if not registro:
        registro = UserContent(user_id=current_user.id, content_id=content_id)
    registro.visto = True
    db.session.add(registro)
    db.session.commit()
    return redirect("/catalogo")

@app.route("/favoritos")
@login_required
def favoritos():
    favoritos = UserContent.query.filter_by(user_id=current_user.id, favorito=True).all()
    return render_template("favoritos.html", favoritos=favoritos)

@app.route("/vistos")
@login_required
def vistos():
    vistos = UserContent.query.filter_by(user_id=current_user.id, visto=True).all()
    return render_template("vistos.html", vistos=vistos)

# -------------------- BUSCADOR --------------------
@app.route("/buscar")
@login_required
def buscar():
    query = request.args.get("q", "")
    # Buscar en títulos de películas y series que contengan la query
    resultados = Content.query.filter(Content.titulo.ilike(f"%{query}%")).all()
    peliculas = [c for c in resultados if c.tipo == "pelicula"]
    series = [c for c in resultados if c.tipo == "series"]
    return render_template("catalogo.html", peliculas=peliculas, series=series)


# -------------------- ESTADÍSTICAS --------------------

@app.route("/estadisticas")
@login_required
def estadisticas():
    total_vistos = UserContent.query.filter_by(user_id=current_user.id, visto=True).count()
    total_favoritos = UserContent.query.filter_by(user_id=current_user.id, favorito=True).count()
    return render_template("estadisticas.html", vistos=total_vistos, favoritos=total_favoritos)

# -------------------- EJECUCIÓN --------------------

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        crear_admin()
        crear_contenidos_prueba()
        app.run(debug=True)