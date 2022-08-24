from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from data import Articles
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from sqlalchemy import create_engine, text
from sqlalchemy.engine import make_url
from datetime import datetime
import pandas as pd


app=Flask(__name__)
db_url = make_url("mssql+pymssql://sa:7890-123-yy@localhost:1433/HOGWARTS")
db_url=db_url.set(username='sa',password='Festivaldocamarao42')
# A cadeia de conexao é formada por dialect[+driver]://user:password@host:port/dbname
engine = create_engine(db_url, pool_size=5, pool_recycle=3600)

conn = engine.connect()

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Festivaldocamarao'
app.config['MYSQL_DB'] = 'HOGWARTS'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/articles')
def articles():
    return render_template('articles.html', articles=Articles)

def get_tabelas():
    return ['animais','pais']

class RegisterForm(Form):
    tabela = StringField('Tabela',[validators.AnyOf(values=get_tabelas(),message='Escolha uma tabela válida!')])

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    return render_template('dashboard.html')

@app.route('/dashboard/animais')
def animais():
    cur = mysql.connection.cursor()

    # Get articles
    result = cur.execute(f"SELECT * FROM Tb_ANIMAIS LIMIT 10")

    animais = cur.fetchall()

    return render_template('animais.html', animais=animais)
    # Close connection
    cur.close()

@app.route('/dashboard/alunos')
def alunos():
    now = datetime.now()
    formatted_now = now.strftime("%A, %d %B, %Y at %X")
    conn = engine.connect()
    sql_text = text("SELECT * FROM dbo.Tb_alunos")
    alunos = conn.execute(sql_text)

    return render_template('alunos.html',alunos=alunos)


@app.route('/article/<string:id>')
def article(id):
    return render_template('article.html', id=id)

if __name__=='__main__':
    app.run(debug=True)
