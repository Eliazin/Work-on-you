<<<<<<< HEAD
# Bibliotecas necessárias
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import check_password_hash

from passlib.hash import pbkdf2_sha256
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__, static_folder='src\\static', template_folder='src\\templates')

app.secret_key = 'key'

# Dados do database(Xampp)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'usuarios'

# Inticializar o MySQL
mysql = MySQL(app)

@app.route('/')
@app.route('/signup', methods=['GET', 'POST'])
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
            msg = 'Por favor preencha o formulário completo'
        # Se o email não for válido, mostrar uma mensagem de erro
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Endereço de e-mail inválido'
        elif (not re.match(r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$", password)):
            msg = 'senha deve conter no mínimo 12 caracteres'
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
    return render_template('signup.html', msg=msg)


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
            return render_template('index.html', msg=msg)
        if not check_password_hash(username, password):
            # Se os dados estão incorretos, demonstrar mensagem de erro( Mais mensagens serão adicionadas)
            msg = 'Senha incorreta'
        if not username or not password:
            msg = 'Por favor preencha todos os campos'
    # Retornar template com mensagem
    return render_template('login.html', msg=msg)

if __name__ == "__main__":
    app.debug = True
    app.run()
=======
# Bibliotecas necessárias
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import check_password_hash

from passlib.hash import pbkdf2_sha256
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__, static_folder='src\\static')

app.secret_key = 'key'

# Dados do database(Xampp)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'usuarios'

# Inticializar o MySQL
mysql = MySQL(app)

@app.route('/')
@app.route('/signup', methods=['GET', 'POST'])
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
        elif not username or not password or not email or not nomeUser:
            msg = 'Por favor preencha o formulário completo'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Endereço de e-mail inválido'
        elif (len(password) < 12 and not re.match(r"/[^A-Za-z0-9]/", password)):
            msg = 'senha deve conter no mínimo 12 caracteres'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Nome de Usuário deve conter apenas letras e números'
        else:
            # Conta não existe e o usuário preencheu com informações válidas, cadastrar no banco
            cursor.execute('INSERT INTO usuarios VALUES (NULL, %s, %s, %s, %s)',
                           (username, email, password, nomeUser))
            mysql.connection.commit()
            msg = 'Você se cadastrou com sucesso'
    elif request.method == 'POST':
        # Formulário vazio
        msg = 'Por favor preencha o formulário completo'
    # Mostrar formulário com mensagem
    return render_template('Signup.html', msg=msg)


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
            session['ID'] = account['ID']
            session['nomeUser'] = account['nomeUser']
            msg = 'Bem vindo!'
            return render_template('index.html', msg=msg)
        if not check_password_hash(username, password):
            # Se os dados estão incorretos, demonstrar mensagem de erro( Mais mensagens serão adicionadas)
            msg = 'Senha incorreta'
        if not username or not password:
            msg = 'Por favor preencha todos os campos'
    # Retornar template com mensagem
    return render_template('login.html', msg=msg)

if __name__ == "__main__":
    app.debug = True
    app.run()
>>>>>>> 4e594480d0d0ba5dd6b94740f64af99bc122b23c
