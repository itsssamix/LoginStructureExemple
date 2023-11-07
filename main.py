from flask import Flask, render_template, redirect, request, flash
import mysql.connector

app = Flask(__name__)


@app.route("/", methods=["POST", "GET"])
def home():
    return render_template("login.html")

@app.route('/usuarios')
def usuarios():
    return render_template('usuarios.html')

@app.route('/cadastrarusuario')
def cadastrar():
    return render_template('cadastrousuario.html')

@app.route("/login", methods=["POST", "GET"])
def login():
    nome = request.form.get('nome')
    senha = request.form.get('senha')
    conect_DB = mysql.connector.connect(host="localhost", database="cadastro", user="root", password="123456")
    if conect_DB.is_connected():
        cursor = conect_DB.cursor()

        # Execute a consulta para buscar os usuários no banco de dados
        cursor.execute('SELECT * FROM usuario;')
        usuariosDB = cursor.fetchall()

        for usuario in usuariosDB:
            usuarioNome = str(usuario[1])
            usuarioSenha = str(usuario[2])

            if usuarioNome == nome and usuarioSenha == senha:

                return redirect('/usuarios')

        else:
            return redirect('/')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastrarusuario():
    if request.method == 'POST':
        nome = request.form['nome']
        senha = request.form['senha']

        conect_DB = mysql.connector.connect(host="localhost", database="cadastro", user="root", password="123456")
        cursor = conect_DB.cursor()
        cursor.execute("INSERT INTO usuario (nome, senha) VALUES (%s, %s)", (nome, senha))
        conect_DB.commit()
        cursor.close()
        conect_DB.close()

    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)
