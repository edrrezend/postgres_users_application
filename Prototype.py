from flask import Flask, render_template, flash, redirect, url_for, Blueprint
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField
from wtforms.validators import DataRequired, EqualTo
from flask_bootstrap import Bootstrap
import psycopg2

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
bootstrap = Bootstrap(app)

# Configurações do banco de dados
DB_HOST = ''
DB_PORT = ''
DB_NAME = ''
DB_USER = ''
DB_PASSWORD = ''

conn = psycopg2.connect(
    host=DB_HOST,
    port=DB_PORT,
    database=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD
)

# Formulário de criação de usuário
class CreateUserForm(FlaskForm):
    nome_usuario = StringField('Nome de usuário', validators=[DataRequired()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    nivel_acesso = SelectField('Nível de acesso', choices=[(1, 'Administrador'), (2, 'Usuário')], coerce=int)

# Formulário de login
class LoginForm(FlaskForm):
    nome_usuario = StringField('Nome de usuário', validators=[DataRequired()])
    senha = PasswordField('Senha', validators=[DataRequired()])

# Blueprint para autenticação e criação de usuários
auth_bp = Blueprint('auth', __name__, url_prefix='/')
@app.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        nome_usuario = form.nome_usuario.data
        senha = form.senha.data
        
        # Autenticação do usuário no banco de dados
        # Verifique as credenciais do usuário no banco de dados
        
        if nome_usuario == 'postgres' and senha == 'Dududb':
            flash('Login bem-sucedido!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Credenciais inválidas. Tente novamente.', 'danger')
    return render_template('login.html', form=form)

@app.route('/index', methods=['GET', 'POST'])
def index():
    form = CreateUserForm()
    if form.validate_on_submit():
        if form.nivel_acesso.data != 1:
            flash('Apenas o administrador pode criar usuários.', 'danger')
            return redirect(url_for('index'))
        
        nome_usuario = form.nome_usuario.data
        senha = form.senha.data
        nivel_acesso = form.nivel_acesso.data
        
        # Insira o código para salvar os dados do novo usuário no banco de dados
        
        flash('Usuário criado com sucesso', 'success')
        return redirect(url_for('index'))
    return render_template('index.html', form=form)

# Registrar o Blueprint de autenticação e criação de usuários
app.register_blueprint(auth_bp)

if __name__ == '__main__':
    app.run(debug=True)
