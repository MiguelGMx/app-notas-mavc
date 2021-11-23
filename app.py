from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import redirect

app = Flask(__name__)
#Habilitando el suo de ORM en la app flask mediante el objeto "db"
db = SQLAlchemy(app)
# postgresql://<nmobre_usuario>:<contra>@<host>:<puerto>/<nombre_basededatos>
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1205@localhost:5432/notas'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
class Notas(db.Model):
	'''Clase Notas'''
	__tablename__ = "notas"
	idNota = db.Column(db.Integer, primary_key = True)
	tituloNota = db.Column(db.String(80))
	cuerpoNota = db.Column(db.String(150))

	def __init__(self,tituloNota,cuerpoNota):
		self.tituloNota = tituloNota
		self.cuerpoNota = cuerpoNota



# --------------------------------------- Vista Index / Menu Principal ----------------------------------------------------------------
@app.route('/')
def index():
	return render_template("index.html")
# --------------------------------------- Vista Crearnostas / Crear Notas ----------------------------------------------------------------
@app.route('/crean')
def crean():
	return render_template("crearnostas.html")

@app.route("/crearnota", methods=['POST'])
def crearnota():
	campotitulo = request.form["campotitulo"]
	campocuerpo = request.form["campocuerpo"]
	notaNueva = Notas(tituloNota=campotitulo,cuerpoNota=campocuerpo)
	db.session.add(notaNueva)
	db.session.commit()
	return render_template("crearnostas.html")#, titulo = campotitulo, cuerpo = campocuerpo
# --------------------------------------- Vista About / Ver Notas / Eliminar -------------------------------------------------------
@app.route("/about")
def about():
	conulta_notas = Notas.query.all()
	for nota in conulta_notas:
		titulo = nota.tituloNota
		cuerpo = nota.tituloNota
	return render_template("about.html", consulta = conulta_notas)

@app.route("/leernotas")
def leernotas():
	conulta_notas = Notas.query.all()
	for nota in conulta_notas:
		titulo = nota.tituloNota
		cuerpo = nota.tituloNota
	return render_template("about.html", consulta = conulta_notas)

@app.route("/eliminarnota/<id>")
def eliminarnota(id):
	Notas.query.filter_by(idNota = int(id)).delete()
	db.session.commit()
	return redirect("/about")
# --------------------------------------- Vista modificarNota / Modificar Notas -----------------------------------------------------
@app.route("/editarnota/<id>")
def editarnota(id):
	nota = Notas.query.filter_by(idNota = int(id)).first()

	db.session.commit()
	return render_template("modificarNota.html", nota = nota)

@app.route("/modificarNota", methods=['POST'])
def modificarNota():
	idnota = request.form['idnota']
	ntitulo = request.form['campotitulo']
	ncuerpo = request.form['campocuerpo']
	nota = Notas.query.filter_by(idNota=int(idnota)).first()
	nota.tituloNota = ntitulo
	nota.cuerpoNota = ncuerpo
	db.session.commit()
	return redirect("/leernotas")
# --------------------------------------- Vista Main general -------------------------------------------------------
if __name__ == "__main__":
	db.create_all()
	app.run()