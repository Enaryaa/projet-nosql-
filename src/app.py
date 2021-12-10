from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/connexion", methods=['POST'])
def connect():

    
    return render_template('connexion.html')


@app.route("/inscription")
def signup():
    return render_template('inscription.html')


@app.route("/post")
def post():
    return render_template('post.html')

@app.route("/consulter")
def consult():
    return render_template('consulter.html')

@app.route("/deco")
def deco():
    return render_template('deco.html')

#def like():
#   return like;


if __name__ == '__main__':
    app.run(port=80, debug=True, host='0.0.0.0')
