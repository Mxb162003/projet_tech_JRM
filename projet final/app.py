from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'
app.debug = True
db = SQLAlchemy(app)
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)



class Espece(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom_commun = db.Column(db.String(100), nullable=False)
    nom_latin = db.Column(db.String(100), nullable=False)
    categorie = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=True)
    image = db.Column(db.String(200), nullable=True)

with app.app_context() :
    db.create_all()
    db.session.commit()
    db.drop_all()
    db.create_all()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/categories', methods=['GET', 'POST'])
def categories():
    if request.method == 'POST':
        nom_commun = request.form['nom_commun']
        nom_latin = request.form['nom_latin']
        categorie = request.form['categorie']
        description = request.form['description']
        image_file = request.files.get('image')
        image_filename = None
        if image_file and image_file.filename != '':
            image_filename = secure_filename(image_file.filename)
            image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], image_filename))
            image = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
        nouvelle = Espece(nom_commun=nom_commun, nom_latin=nom_latin, categorie=categorie, description=description, image=image_filename)
        db.session.add(nouvelle)
        db.session.commit()
        return redirect('/categories')
    
    especes = Espece.query.all()
    return render_template('categories.html', especes=especes)

@app.route('/ajouter', methods=['GET', 'POST'])
def ajouter():
    if request.method == 'POST':
        nom_commun = request.form['nom_commun']
        nom_latin = request.form['nom_latin']
        categorie = request.form['categorie']
        description = request.form['description']
        image_file = request.files.get('image')
        image_filename = None
        if image_file and image_file.filename != '':
            image_filename = secure_filename(image_file.filename)
            image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], image_filename))
            image = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
        nouvelle = Espece(nom_commun=nom_commun, nom_latin=nom_latin, categorie=categorie, description=description, image=image_filename)
        db.session.add(nouvelle)
        db.session.commit()
        return redirect('/categories')
    
    return render_template('categories.html')

@app.route('/test')
def test():
    return render_template('categories.html', especes=[])
