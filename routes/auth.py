from flask import Blueprint, request, render_template, redirect, session, url_for, flash, Markup
from utils.Database import Database

auth = Blueprint('auth', __name__)


@auth.route('/auth')
def Auth():
    return render_template('auth.html')


@auth.route('/auth/login', methods=['POST'])
def login():
    if request.method == 'POST':
        sproc = "[usr].[UserLogin] @Email = ?, @Password= ?"
        user_email = request.form['email']
        params = (user_email, request.form['password'])
        conn = Database.connect()
        cursor = conn.cursor()
        result = Database.execute_sproc(sproc, params, cursor)

        if "Login successful" == result[0][0]:
            query = f"SELECT [UserID] FROM [usr].[User] WHERE [Email] = '{user_email}'"
            result = Database.execute_query(query, cursor)
            conn.close()
            session['user_id'] = result[0][0]
            return redirect(url_for('upload_data.upload_page'))
        else:
            if(result[0][0] == "Incorrect password"):
                flash(Markup(f'{result[0][0]}: <a href="/auth" class="reset-link">Reset password?</a>'))
            else:
                flash(result[0][0])
    return redirect('/auth')


@auth.route('/auth/register', methods=['POST'])
def register():
    if request.method == 'POST':
        if request.form['regPassword'] != request.form['regPassword2']:
            flash('Error: Password does not match')
            return redirect(url_for('auth.Auth'))
        params = (
            request.form['regEmail'],
            request.form['regPassword'],
            request.form['regFirstname'],
            request.form['regLastname'])

        sproc = """[usr].[CreateUser] @Email = ?, @Password= ?, @FirstName = ?, @LastName = ?"""
        conn = Database.connect()
        cursor = conn.cursor()
        info = Database.execute_sproc(sproc, params, cursor)
        cursor.commit()
        conn.close()
        flash(info[0][0])
    return redirect(url_for('auth.Auth'))


@auth.route('/auth/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.Auth'))