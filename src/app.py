from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/index")
def index():
    return render_template('index.html')

@app.route("/connexion")
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


if __name__ == '__main__':
    app.run(port=80, debug=True, host='0.0.0.0')
