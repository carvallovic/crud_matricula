from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

# Conexión MongoDB
client = MongoClient("mongodb+srv://vicarvallo_db_user:Demian260714@cluster0.sib9rg5.mongodb.net/")
db = client["Colegio"]
collection = db["Matriculas"]

@app.route('/')
def home():
    Matriculas = list(collection.find())
    return render_template('index.html', Matriculas=Matriculas)

@app.route('/add', methods=['GET', 'POST'])
def add_registration():
    if request.method == 'POST':
        collection.insert_one({
            'alumno': request.form['alumno'],
            'apoderado': request.form['apoderado'],
            'anio': request.form['anio']
        })
        return redirect(url_for('home'))
    return render_template('add_registration.html')

@app.route('/update/<id>', methods=['GET', 'POST'])
def update_registration(id):
    matricula = collection.find_one({'_id': ObjectId(id)})
    if request.method == 'POST':
        collection.update_one({'_id': ObjectId(id)}, {'$set': {
            'alumno': request.form['alumno'],
            'apoderado': request.form['apoderado'],
            'anio': request.form['anio']
        }})
        return redirect(url_for('home'))
    return render_template('update_registration.html', matricula=matricula)

@app.route('/delete/<id>')
def delete_registration(id):
    collection.delete_one({'_id': ObjectId(id)})
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
