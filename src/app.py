from flask import Flask, render_template, request, redirect, flash, url_for, session
import bcrypt
import psycopg2
from pymongo import MongoClient


app = Flask(__name__)
app.config['SECRET_KEY'] = '78EmLQyrRV'


client = MongoClient('mongodb',27017 )
dbUser=client.user
dbPotin = client.potin

#Postgres
postgresdb = psycopg2.connect(host="postgres-nosql",user="test", password="test",dbname="test")

# methode pour alimenter mongodb
@app.route("/index")
def index():
    return render_template('index.html')

@app.route("/connexion", methods=["POST", "GET"])
def login():
    if request.method == 'POST':
        users = dbUser.user
        login = users.find_one({'pseudo': request.form['pseudo']})
    
        if login is not None:
            if bcrypt.hashpw(request.form['password'].encode('utf-8'), login['password']) == login['password']:
                session['pseudo'] = request.form['pseudo']
                flash("Connexion réussite", 'success')
                return redirect(url_for('index'))

        flash("Mauvais pseudo ou mot de passe", "danger")
        return redirect(url_for('login'))
        
    return render_template('connexion.html')


@app.route("/inscription", methods=["POST", "GET"])
def signup():
    if request.method == 'POST':
        users = dbUser.user
        new_user = users.find_one({"pseudo" :request.form['pseudo']})

        if new_user is None:
            pwd = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
            users.insert_one({
                'pseudo' :  request.form['pseudo'], 
                'password' : pwd
                })
            session['pseudo'] = request.form['pseudo']
            flash("Compte bien créé", 'success')
            return redirect(url_for('index'))

        flash("Pseudo déjà pris", 'danger')
        return redirect(url_for('signup'))

    
    return render_template('inscription.html')


@app.route("/post", methods=["POST", "GET"])
def post():

 if request.method == 'POST':
    if 'pseudo' in session:
        like = 0
        potins = dbPotin.potin
        potins.insert_one({
            'ragot' : request.form['ragot'], 
            'pseudo' : session['pseudo'],
            #'like' : like
        })
        flash("Potin envoyé ! ", 'success')
        return render_template('post.html')
        
    flash("Tu n'es pas autorisé à envoyer des potins", 'danger')
    return redirect(url_for('index'))

 return render_template('post.html')


@app.route("/consulter", methods = ['GET'])
def consult():
    cursordb = postgresdb.cursor()
    cursordb.execute("select * from potin;")
    data = cursordb.fetchall()

    #potins = dbPotin.potin
    # if we don't want to print id then pass _id:0
    #data = potins.find({}, {"_id":0, "ragot": 1, "pseudo": 1 })
    return render_template('consulter.html', data = data)

@app.route("/deco")
def deco():
    session.pop('pseudo', None)
    return redirect(url_for('index'))

#@app.route("/like", methods=["POST", "GET"])
#def like():
    if request.method == 'POST':
        if 'pseudo' in session:
            potins = dbPotin.potin
            potins.update( {'$inc': {'like': 1}})
            return redirect(url_for('consult')) 

        flash("Tu n'es pas connecté ", 'danger')
        return redirect(url_for('index'))
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(port=80, debug=True, host='0.0.0.0')
