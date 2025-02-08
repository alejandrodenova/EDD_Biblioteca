from flask import Flask, render_template, request, redirect, url_for, jsonify, Blueprint
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime
from datetime import datetime

app = Flask(__name__)

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Biblioteca.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicialización de la base de datos
db = SQLAlchemy(app)

class Libro(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(120), nullable=False)
    autor = db.Column(db.String(64))
    fecha_publicacion = db.Column(db.String)
    paginas = db.Column(db.Integer, nullable=False)


@app.route('/')
@app.route('/home')
@app.route('/biblioteca')
def home():
    return render_template('index.html')

@app.route('/listar_libros')
def get_libros():
    libros = Libro.query.all()
    return render_template('Biblioteca/Biblioteca.html', libros=libros)

@app.route('/form_agregar_libro')
def form_agregar_libro():
    return render_template('Biblioteca/Añadir.html')

@app.route('/agregar_libro', methods=['POST'])
def agregar_libro():
    nombre = request.form['nameBook']
    autor = request.form['autorBook']
    fecha_publicacion = request.form['datePublished']
    paginas = int(request.form['numberPages'])

    libro = Libro(nombre=nombre, autor=autor, fecha_publicacion=fecha_publicacion, paginas=paginas)
    db.session.add(libro)
    db.session.commit()

    return redirect(url_for('get_libros'))


#Elimina el libro mediante la ID
@app.route('/eliminar_libro/<int:id>', methods=['POST'])
def eliminar_libro(id):
    libro = Libro.query.get(id)
    if libro:
        db.session.delete(libro)
        db.session.commit()
    return redirect(url_for('get_libros'))



if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Crea las tablas si no existen
    app.run(debug=True)