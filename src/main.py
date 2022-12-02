# Bibliotecas necessárias
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import check_password_hash

from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)

app.secret_key = 'key'

# Dados do database(Xampp)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'usuarios'

# Inticializar o MySQL
mysql = MySQL(app)



@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Mensagem caso haja algum erro
    msg = ''
    # Checar se o usuário preencheu os campos
    if request.method == 'POST' and 'nomeUser' in request.form and 'senha' in request.form:
        # Variáveis de acesso
        username = request.form['nomeUser']
        password = request.form['senha']
        # Verificar os dados no banco de dados
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM usuarios WHERE nomeUser = % s AND senha = % s', (username, password, ))
        account = cursor.fetchone()
        # Verificar se a conta existe
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['nomeUser'] = account['nomeUser']
            msg = 'Bem vindo!'
            return render_template('home.html', msg=msg)
        if not check_password_hash(username, password):
            # Se os dados estão incorretos, demonstrar mensagem de erro( Mais mensagens serão adicionadas)
            msg = 'Senha incorreta'
        if not username or not password:
            msg = 'Por favor preencha todos os campos'
    # Retornar template com mensagem
    return render_template('login.html', msg=msg)

@app.route('/Signup', methods=['GET', 'POST'])
def signup():
    # Mensagem caso haja algum erro
    msg = ''
    # Checar se o usuário preencheu os campos
    if request.method == 'POST' and 'nome' in request.form and 'email' in request.form and 'senha' in request.form and 'nomeUser' in request.form:
        # Variáveis de acesso
        username = request.form['nome']
        password = request.form['senha']
        email = request.form['email']
        nomeUser = request.form['nomeUser']
        # Verificar se a conta existe no banco
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM usuarios WHERE nome = % s and senha = % s and email = % s and nomeUser = % s',
                       (username, password, email, nomeUser))
        account = cursor.fetchone()
        # Se a conta já existir, mostrar uma mensagem de erro
        if account:
            msg = 'Usuário já existente'
        # Se o formulário não for preenchido, mostrar uma mensagem de erro
        elif not username or not password or not email or not nomeUser:
            msg = '\n\nPor favor preencha o formulário completo'
        # Se o email não for válido, mostrar uma mensagem de erro
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Endereço de e-mail inválido'
        elif (not re.match(r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$", password)):
            msg = 'senha deve conter no mínimo 8 caracteres,\n uma letra e um caracter especial'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Nome de Usuário deve conter apenas letras e números'
        else:
            # Conta não existe e o usuário preencheu com informações válidas, cadastrar no banco
            cursor.execute('INSERT INTO usuarios VALUES (NULL, %s, %s, %s, %s)',
                           (username, password, email, nomeUser))
            mysql.connection.commit()
            msg = 'Você se cadastrou com sucesso'
    elif request.method == 'POST':
        # Formulário vazio
        msg = 'Por favor preencha o formulário completo'
    # Mostrar formulário com mensagem
    return render_template('Signup.html', msg=msg)

@app.route('/exercicios')
def exercicios():
    return render_template('exercicios.html')

@app.route('/filmes')
def filmes():
    return render_template('filmes.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/livros')
def livros():
    return render_template('livros.html')

@app.route('/mindset')
def mindset():
    return render_template('mindset.html')

@app.route('/musicas')
def musicas():
    return render_template('musicas.html')

@app.route('/organizacao')
def organizacao():
    return render_template('organização.html')

@app.route('/planner')
def planner():
    return render_template('planner.html')

@app.route('/alimentacao')
def alimentacao():
    return render_template('alimentacao.html')

@app.route('/cardio')
def cardio():
    return render_template('cardio.html')

@app.route('/aerobico')
def aerobico():
    return render_template('aerobico.html')

@app.route('/muscu')
def muscu():
    return render_template('muscu.html')


if __name__ == "__main__":
    app.debug = True
    app.run()