# all the imports
import sqlite3, os, json, time
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from contextlib import closing

from werkzeug import secure_filename

from werkzeug.contrib.cache import SimpleCache

from wtforms import Form, BooleanField, TextField, PasswordField, validators


# configuration
DATABASE = '/tmp/honeycomb.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'
CACHE_TIMEOUT = 3

UPLOAD_FOLDER = '/tmp/'
ALLOWED_EXTENSIONS = set(['txt','pdf','zip','tar','doc','docx'])

# create the application
app = Flask(__name__)
app.config.from_object(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

cache = SimpleCache()

class RegistrationForm(Form):
    username = TextField('Username', [validators.Length(min=4, max=25)])
    email = TextField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('New Password', [
        validators.Required(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the TOS', [validators.Required()])

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        user = [form.username.data, form.email.data,
                    form.password.data]
        # TODO: save user info in another db
        #db_session.add(user)
        flash('Thanks for registering')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.before_request
def return_cached():
    # if GET and POST not empty
    if not request.values:
        response = cache.get(request.path)
        if response: 
            return response

@app.after_request
def cache_response(response):
    if not request.values:
        cache.set(request.path, response, CACHE_TIMEOUT)
    return response

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

@app.route('/')
def show_entries():
    cur = g.db.execute('select title, text from entries order by id desc')
    entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    return render_template('show_entries.html', entries=entries)    

@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    g.db.execute('insert into entries (title, text) values (?, ?)',
                 [request.form['title'], request.form['text']])
    g.db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))

@app.route('/insert', methods=['POST'])
def insert_entry():
    g.db.execute('insert into entries (title, text) values (?, ?)',
                 [request.form['title'], request.form['text']])
    g.db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))

@app.route('/select', methods=['POST'])
def select_entries():
    cur = g.db.execute('select title, text from entries where title=?',
                 [request.form['title']])
    entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    return json.dumps(entries)

@app.route('/delete', methods=['POST'])
def delete_entries():
    g.db.execute('delete from entries where title=?',
                 [request.form['title']])
    g.db.commit()
    return "The entries were successfully deleted"

@app.route('/querying', methods=['POST'])
def querying_entries():
    cur = g.db.execute(request.form['querying'])
    entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    return json.dumps(entries)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route("/upload", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('index'))
    return """
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    <p>%s</p>
    """ % "<br>".join(os.listdir(app.config['UPLOAD_FOLDER'],))

if __name__ == '__main__':
    app.run()
