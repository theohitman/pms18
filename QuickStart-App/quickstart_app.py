# This file contains an example Flask-User application.
# To keep the example simple, we are applying some unusual techniques:
# - Placing everything in one file
# - Using class-based configuration (instead of file-based configuration)
# - Using string-based templates (instead of file-based templates)

import datetime
from flask import Flask, request, flash, url_for, redirect, render_template, render_template_string
from flask.templating import render_template
from flask_sqlalchemy import SQLAlchemy
from flask_user import current_user, login_required, roles_required, UserManager, UserMixin
from flask_mail import Mail, Message
# Class-based application configuration


class ConfigClass(object):
    """ Flask application config """

    # Flask settings
    SECRET_KEY = 'This is an INSECURE secret!! DO NOT use this in production!!'

    # Flask-SQLAlchemy settings
    # File-based SQL database
    SQLALCHEMY_DATABASE_URI = 'sqlite:///quickstart_app.sqlite'
    SQLALCHEMY_TRACK_MODIFICATIONS = False    # Avoids SQLAlchemy warning

    # Flask-User settings
    USER_APP_NAME = "Beekeeper App"
    USER_ENABLE_EMAIL = False        # Disable email authentication
    USER_ENABLE_USERNAME = True    # Enable username authentication
    USER_REQUIRE_RETYPE_PASSWORD = False    # Simplify register form
    USER_EMAIL_SENDER_NAME = USER_APP_NAME
    USER_EMAIL_SENDER_EMAIL = "melishop.info@gmail.com"

    # Flask-Mail SMTP server settings
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = False
    MAIL_USE_TLS = False
    MAIL_USERNAME = '"melishop.info@gmail.com'
    MAIL_PASSWORD = 'melishop123'
    MAIL_DEFAULT_SENDER = 'melishop.info@gmail.com'


def create_app():
    """ Flask application factory """

    # Create Flask app load app.config
    app = Flask(__name__)
    app.config.from_object(__name__+'.ConfigClass')
    mail_settings = {
        "MAIL_SERVER": ConfigClass.MAIL_SERVER,
        "MAIL_PORT": ConfigClass.MAIL_PORT,
        "MAIL_USE_TLS": ConfigClass.MAIL_USE_TLS,
        "MAIL_USE_SSL": ConfigClass.MAIL_USE_SSL,
        "MAIL_USERNAME": ConfigClass.MAIL_USERNAME,
        "MAIL_PASSWORD": ConfigClass.MAIL_PASSWORD,
        "MAIL_DEFAULT_SENDER": ConfigClass.MAIL_DEFAULT_SENDER
    }

    app.config.update(mail_settings)

    # Initialize Flask-SQLAlchemy
    db = SQLAlchemy(app)

    # Define the User data-model.
    # NB: Make sure to add flask_user UserMixin !!!
    class User(db.Model, UserMixin):
        __tablename__ = 'users'
        id = db.Column(db.Integer, primary_key=True)
        active = db.Column('is_active', db.Boolean(),
                           nullable=False, server_default='1')

        # User authentication information. The collation='NOCASE' is required
        # to search case insensitively when USER_IFIND_MODE is 'nocase_collation'.
        username = db.Column(
            db.String(100, collation='NOCASE'), nullable=False, unique=True)
        email = db.Column(db.String(255, collation='NOCASE'),
                          nullable=True)
        email_confirmed_at = db.Column(db.DateTime())
        password = db.Column(db.String(255), nullable=False, server_default='')

        # User information
        first_name = db.Column(
            db.String(100, collation='NOCASE'), nullable=False, server_default='')
        last_name = db.Column(
            db.String(100, collation='NOCASE'), nullable=False, server_default='')

        # Define the relationship to Role via UserRoles
        roles = db.relationship('Role', secondary='user_roles')

    # Define the Role data-model
    class Role(db.Model):
        __tablename__ = 'roles'
        id = db.Column(db.Integer(), primary_key=True)
        name = db.Column(db.String(50), unique=True)

    # Define the UserRoles association table
    class UserRoles(db.Model):
        __tablename__ = 'user_roles'
        id = db.Column(db.Integer(), primary_key=True)
        user_id = db.Column(db.Integer(), db.ForeignKey(
            'users.id', ondelete='CASCADE'))
        role_id = db.Column(db.Integer(), db.ForeignKey(
            'roles.id', ondelete='CASCADE'))

    class members(db.Model):
        id = db.Column('member_id', db.Integer, primary_key=True)
        beekeeper_id = db.Column(db.String(10), unique=True)
        name = db.Column(db.String(100))
        city = db.Column(db.String(50))
        country = db.Column(db.String(200))
        address = db.Column(db.String(255))
        production_area = db.Column(db.String(255))
        beehives = db.Column(db.Integer)

        def __init__(self, beekeeper_id, name, city, country, address, production_area, beehives):
            self.beekeeper_id = beekeeper_id
            self.name = name
            self.city = city
            self.country = country
            self.address = address
            self.production_area = production_area
            self.beehives = beehives

    # Setup Flask-User and specify the User data-model
    user_manager = UserManager(app, db, User)

    # Create all database tables
    db.create_all()

    # Create 'member@example.com' user with no roles
    # if not User.query.filter(User.email == 'member@example.com').first():
    #     user = User(
    #         email='member@example.com',
    #         email_confirmed_at=datetime.datetime.utcnow(),
    #         password=user_manager.hash_password('Password1'),
    #     )
    #     db.session.add(user)
    #     db.session.commit()

    # Create 'admin@example.com' user with 'Admin' and 'Agent' roles
    if not User.query.filter(User.email == 'itp20132@hua.gr').first():
        user = User(
            username='admin',
            email='itp20132@hua.gr',
            email_confirmed_at=datetime.datetime.utcnow(),
            password=user_manager.hash_password('Admin1'),
        )
        user.roles.append(Role(name='Admin'))
        db.session.add(user)
        db.session.commit()
    # The Home page is accessible to anyone

    @app.route('/')
    def home_page():
        return render_template('home_page.html')

    # The Members page is only accessible to authenticated users via the @login_required decorator
    @app.route('/members')
    @login_required
    @roles_required('Admin')
    def member_page():
        return render_template('members_all.html', members=members.query.all())
        # String-based templates
        # return render_template_string("""
        #     {% extends "flask_user_layout.html" %}
        #     {% block content %}
        #         <h2>Members page</h2>
        #         <p><a href={{ url_for('user.register') }}>Register</a></p>
        #         <p><a href={{ url_for('user.login') }}>Sign in</a></p>
        #         <p><a href={{ url_for('home_page') }}>Home page</a> (accessible to anyone)</p>
        #         <p><a href={{ url_for('member_page') }}>Member page</a> (login required)</p>
        #         <p><a href={{ url_for('user.logout') }}>Sign out</a></p>
        #     {% endblock %}
        #     """)

    @app.route('/new_member', methods=['GET', 'POST'])
    @login_required
    def new_member_page():
        if request.method == 'POST':
            if not request.form['name'] or not request.form['city'] or not request.form['country'] or not request.form['production_area'] or not request.form['beekeeper_id'] or not request.form['address']:
                flash('Please enter all the fields', 'error')
            else:
                member = members(request.form['beekeeper_id'],
                                 request.form['name'],
                                 request.form['city'],
                                 request.form['country'],
                                 request.form['address'],
                                 request.form['production_area'],
                                 request.form['beehives'])
                db.session.add(member)
                db.session.commit()
                flash('Record was successfully added')
                if current_user.has_roles("Admin"):
                    return redirect(url_for('member_page'))
                else:
                    return redirect(url_for('home_page'))
        return render_template('new_member.html')
    return app


# Start development web server
if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
