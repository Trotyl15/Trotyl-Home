from random import choices
from secrets import choice
from unicodedata import name
from flask import Flask, redirect, render_template, request, request, redirect, url_for
from flask_sqlalchemy import  SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, SelectField
from wtforms.validators import InputRequired, Length, ValidationError

app = Flask(__name__, static_folder = 'src')
# app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///test.db'
app.config['SQLALCHEMY_DATABASE_URI']=os.getenv('DATABASE_URL')
db=SQLAlchemy(app)
app.config['SECRET_KEY']='thisissecret'

@app.route('/')
def home():
	return render_template('index.html')

class Project(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(200), nullable=False)
    link=db.Column(db.String(200), nullable=True)
    description=db.Column(db.String(255), nullable=True)
    icon=db.Column(db.Integer, nullable=True)
    image=db.Column(db.String(255), nullable=True)

class ProjectForm(FlaskForm):
    name=StringField(validators=[InputRequired(), Length(
        min=4)], render_kw={"placeholder": " name"})
    link=StringField(render_kw={"placeholder": " link"})
    description=StringField(render_kw={"placeholder": " description"})
    icon=SelectField(choices=[(1, "blank"), (2, "github"), (3, "external")], default=(1, "blank"))
    image=StringField(render_kw={"placeholder": " image"})

    submit = SubmitField("Submit")

@app.route('/projects/admin/create',  methods=['GET', 'POST'])
def projects_create():
    form=ProjectForm()
    if form.validate_on_submit():
        new_project=Project(name=form.name.data, link=form.link.data, description=form.description.data, icon=form.icon.data, image=form.image.data)
        db.session.add(new_project)
        db.session.commit()
        return redirect(url_for('projects', _anchor='bottom'))
    return render_template('projectscreate.html',form=form)


@app.route('/projects',  methods=['GET', 'POST'])
def projects():
    projects=Project.query.order_by(Project.id).all()
    return render_template('projects.html', projects=projects)

@app.route('/connect')
def connect():
    return render_template('connect.html')

@app.route('/resume.pdf')
def resume():
    return render_template('resume.pdf')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
	app.run(debug=True)

    
