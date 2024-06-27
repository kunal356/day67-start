from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField
from datetime import date

'''
Make sure the required packages are installed: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from the requirements.txt for this project.
'''

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)
ckeditor = CKEditor(app)

# CREATE DATABASE


class Base(DeclarativeBase):
    pass


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# CONFIGURE TABLE
class BlogPost(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(
        String(250), unique=True, nullable=False)
    subtitle: Mapped[str] = mapped_column(String(250), nullable=False)
    date: Mapped[str] = mapped_column(String(250), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)


class AddForm(FlaskForm):
    title = StringField('Blog Post Title', validators=[DataRequired()])
    sub_title = StringField('Subtitle', validators=[DataRequired()])
    author = StringField('Your Name', validators=[DataRequired()])
    img_url = StringField('Blog Image Url', validators=[DataRequired()])
    body = CKEditorField('Content')
    submit = SubmitField('Submit')


with app.app_context():
    db.create_all()


@app.route('/')
def get_all_posts():
    # TODO: Query the database for all the posts. Convert the data to a python list.
    all_posts = db.session.execute(db.select(BlogPost)).scalars().all()
    posts = []
    for post in all_posts:
        posts.append(post)
    return render_template("index.html", all_posts=posts)


# TODO: Add a route so that you can click on individual posts.
@app.route('/post/<post_id>')
def show_post(post_id):
    # TODO: Retrieve a BlogPost from the database based on the post_id
    requested_post = db.get_or_404(BlogPost, post_id)
    return render_template("post.html", post=requested_post)


# TODO: add_new_post() to create a new blog post
@app.route('/new-post', methods=['GET', 'POST'])
def add_new_post():
    form = AddForm()
    if form.validate_on_submit():
        new_blog = BlogPost(
            title=form.title.data,
            subtitle=form.sub_title.data,
            author=form.author.data,
            img_url=form.img_url.data,
            body=form.body.data,
            date=date.today().strftime("%B %d, %Y")
        )
        db.session.add(new_blog)
        db.session.commit()
        return redirect(url_for("get_all_posts"))
    return render_template("make-post.html", form=form, mode="add")


# TODO: edit_post() to change an existing blog post
@app.route('/edit-post/<post_id>', methods=['POST', 'GET'])
def edit_post(post_id):
    post_to_edit = db.get_or_404(BlogPost, post_id)
    form = AddForm(
        title=post_to_edit.title,
        sub_title=post_to_edit.subtitle,
        author=post_to_edit.author,
        img_url=post_to_edit.img_url,
        body=post_to_edit.body,

    )
    if form.validate_on_submit():
        post_to_edit.title = form.title.data
        post_to_edit.subtitle = form.sub_title.data
        post_to_edit.author = form.author.data
        post_to_edit.img_url = form.img_url.data
        post_to_edit.body = form.body.data
        db.session.commit()
        return redirect(url_for('show_post', post_id=post_id))

    return render_template("make-post.html", form=form, mode="edit")


# TODO: delete_post() to remove a blog post from the database
@app.route('/delete-post/<post_id>', methods=['POST', 'GET', 'DELETE'])
def delete_post(post_id):
    post_to_delete = db.get_or_404(BlogPost, post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('get_all_posts'))
    # Below is the code from previous lessons. No changes needed.


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True, port=5003)
