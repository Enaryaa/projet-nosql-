from flask import Flask, render_template, request, redirect, flash, url_for, session
import bcrypt
import psycopg2
from pymongo import MongoClient


app = Flask(__name__)
app.config['SECRET_KEY'] = '78EmLQyrRV'

#MongoDB
client = MongoClient('mongodb',27017 )
dbUser=client.user
dbLike = client.like

#Postgres
postgresdb = psycopg2.connect(host="postgres-nosql",user="test", password="test",dbname="test")

#Fonction qui permet de savoir si un utilisateur a déja liké un post
def getLike():
    likes = dbLike.like
    user = likes.find_one({"pseudo" : session['pseudo'], "id_potin": request.args["id"] })

    if user is None:
        likes.insert_one({
            'id_potin' : request.args["id"],
            'pseudo' : session['pseudo']
        })
        return True


@app.route("/index")
def index():
    return render_template('index.html')

#Fonction de connexion en pymongo
@app.route("/connexion", methods=["POST", "GET"])
def login():
    if request.method == 'POST':
        users = dbUser.user
        #vérifie si le pseudo existe bien
        login = users.find_one({'pseudo': request.form['pseudo']})
    
        if login is not None:
            #vérifie le mot de passe
            if bcrypt.hashpw(request.form['password'].encode('utf-8'), login['password']) == login['password']:
                session['pseudo'] = request.form['pseudo']
                flash("Connexion réussite", 'success')
                return redirect(url_for('index'))

        flash("Mauvais pseudo ou mot de passe", "danger")
        return redirect(url_for('login'))
        
    return render_template('connexion.html')


#fonction d'inscription d'un utilisateur en pymongo
@app.route("/inscription", methods=["POST", "GET"])
def signup():
    if request.method == 'POST':
        users = dbUser.user
        #permet de savoir si le pseudo est déjà pris
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

#Permet de poster un commentaire / anecdote / ragot en psycopg2 (postgres). Il est obligatoire d'être connecté
@app.route("/post", methods=["POST", "GET"])
def post():
 if request.method == 'POST':
    if 'pseudo' in session:
        cursordb = postgresdb.cursor()
        cursordb.execute("select count(*) from potin;")
        #vérifie si la checkbox anonyme est cochée et renvoie un boolean
        checked = 'anonyme' in request.form
        result=cursordb.fetchone()
        nb_potins=result[0]
        #fait la query pour insert les données relatives à un post
        cursordb.execute("insert into potin values(%s,%s,0,%s,%s);",(int(nb_potins+1),request.form['ragot'],session['pseudo'], checked))
        postgresdb.commit()
   
        flash("Potin envoyé ! ", 'success')
        return render_template('post.html')
        
    flash("Tu n'es pas autorisé à envoyer des potins", 'danger')
    return redirect(url_for('index'))

 return render_template('post.html')

#Permet de consulter les postes faits
@app.route("/consulter", methods = ['GET'])
def consult():
    cursordb = postgresdb.cursor()
    cursordb.execute("select * from potin order by id_potin;")
    data = cursordb.fetchall()
    return render_template('consulter.html', data = data)

@app.route("/deco")
def deco():
    session.pop('pseudo', None)
    return redirect(url_for('index'))

#Permet de liker les posts postés. L'utilisateur ne peut liker qu'un seul post et cela ne peut se faire qu'une fois connecté
@app.route("/like", methods=["POST", "GET"])
def like():
    if request.method == 'POST':
        if 'pseudo' in session:
            cursordb = postgresdb.cursor()
            if getLike() == True:
                cursordb.execute("UPDATE potin SET nombre_likes = nombre_likes+1 where id_potin= %s;",request.args["id"])
                postgresdb.commit()
                flash(" Post liké ! ", 'success')
                return redirect(url_for('consult')) 
            flash("Tu as déjà aimé ce post ! ", 'warning')
            return redirect(url_for('consult'))

        flash("Tu n'es pas connecté ", 'danger')
        return redirect(url_for('consult'))
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(port=80, debug=True, host='0.0.0.0')
