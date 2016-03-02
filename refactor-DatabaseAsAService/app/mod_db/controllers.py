# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for

# Import the database object from the main app module
from app import db

# Import module forms
from app.mod_db.forms import RegistrationForm

# Import module models (i.e. User)
from app.mod_auth.models import User

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_db = Blueprint('db', __name__, url_prefix='/db')

# Set the route and accepted methods
@mod_db.route('/register', methods=['GET', 'POST'])
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

@mod_db.route('/')
def show_entries():
    cur = g.db.execute('select title, text from entries order by id desc')
    entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    return render_template('show_entries.html', entries=entries)    

@mod_db.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    g.db.execute('insert into entries (title, text) values (?, ?)',
                 [request.form['title'], request.form['text']])
    g.db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))

@mod_db.route('/insert', methods=['POST'])
def insert_entry():
    g.db.execute('insert into entries (title, text) values (?, ?)',
                 [request.form['title'], request.form['text']])
    g.db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))

@mod_db.route('/select', methods=['POST'])
def select_entries():
    cur = g.db.execute('select title, text from entries where title=?',
                 [request.form['title']])
    entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    return json.dumps(entries)

@mod_db.route('/delete', methods=['POST'])
def delete_entries():
    g.db.execute('delete from entries where title=?',
                 [request.form['title']])
    g.db.commit()
    return "The entries were successfully deleted"

@mod_db.route('/querying', methods=['POST'])
def querying_entries():
    cur = g.db.execute(request.form['querying'])
    entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    return json.dumps(entries)

@mod_db.route('/login', methods=['GET', 'POST'])
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

@mod_db.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))
