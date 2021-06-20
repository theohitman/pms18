# This file contains an example Flask-User application.
# To keep the example simple, we are applying some unusual techniques:
# - Placing everything in one file
# - Using class-based configuration (instead of file-based configuration)
# - Using string-based templates (instead of file-based templates)

from flask import Flask, request, flash, url_for, redirect, render_template, render_template_string
from flask.templating import render_template
from flask_sqlalchemy import SQLAlchemy
from flask_user import current_user, login_required, roles_required, UserManager, UserMixin
from flask_mail import Mail, Message
from werkzeug.utils import secure_filename
import os
import datetime
import owncloud
from dotenv import load_dotenv

# load dotenv in the base root
APP_ROOT = os.path.dirname(__file__)   # refers to application_top
dotenv_path = os.path.join(APP_ROOT, '.env')
load_dotenv(dotenv_path)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}

# Class-based application configuration


class ConfigClass(object):
    """ Flask application config """

    # Flask settings
    SECRET_KEY = os.getenv("SECRET_KEY")

    # OwnCloud settings
    OWNCLOUD_USERNAME = os.getenv("OWNCLOUD_USERNAME")
    OWNCLOUD_PASSWORD = os.getenv("OWNCLOUD_PASSWORD")
    OWNCLOUD_URL = os.getenv("OWNCLOUD_URL")
    OWNCLOUD_FOLDER = os.getenv("OWNCLOUD_FOLDER")

    # Flask-SQLAlchemy settings
    # File-based SQL database
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv(
        "SQLALCHEMY_TRACK_MODIFICATIONS")    # Avoids SQLAlchemy warning

    # Flask-User settings
    USER_APP_NAME = os.getenv("USER_APP_NAME")
    USER_ENABLE_EMAIL = False        # Disable email authentication
    USER_ENABLE_USERNAME = True    # Enable username authentication
    USER_REQUIRE_RETYPE_PASSWORD = False    # Simplify register form
    USER_EMAIL_SENDER_NAME = USER_APP_NAME
    USER_EMAIL_SENDER_EMAIL = os.getenv("MAIL_DEFAULT_SENDER")

    # Flask-Mail SMTP server settings
    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_PORT = os.getenv("MAIL_PORT")
    MAIL_USE_SSL = os.getenv("MAIL_USE_SSL")
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS")
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER")

    #MAIL_DEBUG : app.debug
    #MAIL_MAX_EMAILS : None
    #MAIL_SUPPRESS_SEND : app.testing
    #MAIL_ASCII_ATTACHMENTS : False


def create_app():
    """ Flask application factory """

    # Create Flask app load app.config
    app = Flask(__name__)
    app.config.from_object(__name__+'.ConfigClass')
    mail_settings = {
        "MAIL_SERVER": ConfigClass.MAIL_SERVER,
        "MAIL_PORT": ConfigClass.MAIL_PORT,
        "MAIL_USE_TLS": False,
        "MAIL_USE_SSL": False,
        "MAIL_USERNAME": ConfigClass.MAIL_USERNAME,
        "MAIL_PASSWORD": ConfigClass.MAIL_PASSWORD,
        "MAIL_DEFAULT_SENDER": ConfigClass.MAIL_DEFAULT_SENDER
    }

    app.config.update(mail_settings)

    oc = owncloud.Client(ConfigClass.OWNCLOUD_URL)
    oc.login(ConfigClass.OWNCLOUD_USERNAME, ConfigClass.OWNCLOUD_PASSWORD)
    oc.mkdir(ConfigClass.OWNCLOUD_FOLDER)

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
            db.String(100), nullable=False, unique=True)
        email = db.Column(db.String(255), nullable=True)
        email_confirmed_at = db.Column(db.DateTime())
        password = db.Column(db.String(255), nullable=False, server_default='')

        # User information
        first_name = db.Column(
            db.String(100), nullable=False, server_default='')
        last_name = db.Column(
            db.String(100), nullable=False, server_default='')

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

    class ApplicationForms(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        beekeeper_id = db.Column(db.String(10), nullable=False)
        name = db.Column(db.String(100))
        city = db.Column(db.String(50))
        country = db.Column(db.String(200))
        address = db.Column(db.String(255))
        production_area = db.Column(db.String(255))
        img_url = db.Column(db.String(255))
        beehives = db.Column(db.Integer)

        def __init__(self, beekeeper_id, name, city, country, address, production_area, beehives, img_url):
            self.beekeeper_id = beekeeper_id
            self.name = name
            self.city = city
            self.country = country
            self.address = address
            self.production_area = production_area
            self.img_url = img_url
            self.beehives = beehives

    # Setup Flask-User and specify the User data-model
    user_manager = UserManager(app, db, User)

    # Create all database tables
    db.create_all()

    mail = Mail(app)

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

    def allowed_file(filename):
        return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    @app.route('/')
    def home_page():
        return render_template('home_page.html')

    # The Members page is only accessible to authenticated users via the @login_required decorator
    @app.route('/forms', methods=['GET', 'POST'])
    @login_required
    @roles_required('Admin')
    def forms_page():
        if request.method == 'POST':
            form = ApplicationForms.query.filter_by(id=request.form['id']).first()
            db.session.delete(form)
            db.session.commit()
            flash('Record was successfully deleted', 'success')
        return render_template('forms_all.html', forms=ApplicationForms.query.all())
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

    @app.route('/new_form', methods=['GET', 'POST'])
    @login_required
    def new_form_page():
        if request.method == 'POST':
            if not request.form['name'] or not request.form['city'] or not request.form['country'] or not request.form['production_area'] or not request.form['beekeeper_id'] or not request.form['address']:
                flash('Please enter all the fields', 'error')
            elif 'image' not in request.files:
                    flash('No image found')
                    return redirect(request.url)
            else:
                file = request.files['image']
                if file.filename == '':
                    flash('No selected image')
                    return redirect(request.url)
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    filepath = os.path.join(f'{APP_ROOT}\\temp', filename)
                    file.save(filepath)
                    if oc.put_file(f'{ConfigClass.OWNCLOUD_FOLDER}/{filename}', filepath):
                    #if oc.put_file_contents(f'{ConfigClass.OWNCLOUD_FOLDER}/{filename}', file):
                        flash('file uploaded')
                    else:
                        flash('file fail to upload')
                        return redirect(request.url)
                    os.remove(filepath)
                    link_info = oc.share_file_with_link(f'{ConfigClass.OWNCLOUD_FOLDER}/{filename}')                    
                    form = ApplicationForms(request.form['beekeeper_id'],
                                            request.form['name'],
                                            request.form['city'],
                                            request.form['country'],
                                            request.form['address'],
                                            request.form['production_area'],
                                            request.form['beehives'],
                                            link_info.get_link())
                    db.session.add(form)
                    db.session.commit()
                    msg = Message(ConfigClass.USER_APP_NAME, recipients=[
                                current_user.email, 'itp20132@hua.gr'])
                    msg.html = f'You Forms has been submitted.<br/>{form.beekeeper_id}<br/>{form.name}<br/>{form.city}<br/>{form.country}<br/>{form.address}<br/>{form.production_area}<br/>{form.beehives}'

                    try:
                        mail.send(msg)
                    except os.error as e:
                        flash(f"Error:{e}", 'warning')

                    flash('Record was successfully added', 'success')
                    if current_user.has_roles("Admin"):
                        return redirect(url_for('forms_page'))
                    else:
                        return redirect(url_for('home_page'))
        return render_template('new_form.html')
    return app


# Start development web server
if __name__ == '__main__':
    app = create_app()
    app.run(host='localhost', port=5000, debug=True)
