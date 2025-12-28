import os
from random import choices
from secrets import choice
from unicodedata import name
from flask import Flask, redirect, render_template, request, request, redirect, url_for
from flask_sqlalchemy import  SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, SelectField
from wtforms.validators import InputRequired, Length, ValidationError
from vitwo_content import (
    VITWO_LANGUAGE_CONTENT,
    VITWO_SUPPORT_COPY,
    APPLE_BADGE_LANG,
)

app = Flask(__name__, static_folder = 'src')
# app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///test.db'
app.config['SQLALCHEMY_DATABASE_URI']=os.getenv('DATABASE_URL')
db=SQLAlchemy(app)
app.config['SECRET_KEY']='thisissecret'

@app.route('/')
def home():
	return render_template('index.html')

@app.route('/vitwo')
def vitwo_root_redirect():
    return redirect(url_for('vitwo_landing_lang', lang_code='en'))

@app.route('/vitwo/support')
def vitwo_support_root_redirect():
    return redirect(url_for('vitwo_support', lang_code='en'))

@app.route('/<lang_code>/vitwo')
def vitwo_landing_lang(lang_code):
    lang_key = (lang_code or "").lower()
    content = VITWO_LANGUAGE_CONTENT.get(lang_key)
    if not content:
        return redirect(url_for('vitwo_landing_lang', lang_code='en'))

    region, badge_lang = APPLE_BADGE_LANG.get(lang_key, APPLE_BADGE_LANG["en"])
    links = {
        "app_store_link": f"https://apps.apple.com/{region}/app/vitwo-sync-watch-together/id6756282977?itscg=30200&itsct=apps_box_badge&mttnsubad=6756282977",
        "app_store_badge": f"https://toolbox.marketingtools.apple.com/api/v2/badges/download-on-the-app-store/black/{badge_lang}?releaseDate=1765929600",
        "chrome": "https://chromewebstore.google.com/detail/vitwo/ldkgjjafibdipikaopgipdkaifjngblc",
        "edge": "https://microsoftedge.microsoft.com/addons/detail/vitwo/dendgmbokdpdoemdebmhcefcmkbchpdk",
    }

    return render_template(
        'vitwo/info.html',
        content=content,
        lang_code=lang_key,
        links=links,
        languages=VITWO_LANGUAGE_CONTENT,
    )

@app.route('/<lang_code>/vitwo/support')
def vitwo_support(lang_code):
    lang_key = (lang_code or "").lower()
    if lang_key not in VITWO_LANGUAGE_CONTENT:
        return redirect(url_for('vitwo_support', lang_code='en'))
    marketing_link = url_for('vitwo_landing_lang', lang_code=lang_key)
    return render_template(
        'vitwo/support.html',
        marketing_link=marketing_link,
        labels=VITWO_LANGUAGE_CONTENT[lang_key]["labels"],
        copy=VITWO_SUPPORT_COPY[lang_key],
        languages=VITWO_LANGUAGE_CONTENT,
        lang_code=lang_key,
    )

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

    
