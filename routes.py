from flask import Flask, render_template, request, redirect, flash
from forms import AddDogForm, RegisterForm, LogInForm
import os
from model import Dog, User, Comment
from configs import app, db
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.security import check_password_hash

@app.route('/')
def index():
    comments = Comment.query.all()
    comment_by_first_user = Comment.query.filter_by(user_id=1).first()
    dogs = Dog.query.all()
    return render_template("about.html", dogs=dogs)


@app.route("/detailed_info/<int:dog_id>", methods=["GET", "POST"])
@login_required
def detailed_info(dog_id):

    selected_dog = Dog.query.get(dog_id)
    print(selected_dog)
    if request.method == "POST":
        content = request.form["content"]
        if current_user.is_authenticated:
            comment = Comment(content=content, user_id=current_user.id, product_id=dog_id)
            db.session.add(comment)
            db.session.commit()
            return redirect (f"/detailed_info/{dog_id}")
    print(selected_dog.comment)
    return render_template("dog_details.html", dog=selected_dog)




@app.route("/add_dog", methods=["GET", "POST"])
@login_required
def add_dog():
    form = AddDogForm()
    if request.method == "POST":
        file = request.files['img']
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        dog = Dog(name=form.name.data, img=filename, description=form.description.data, topic=form.topic.data)
        db.session.add(dog)
        db.session.commit()
        return redirect("/")
    return render_template("add_dog.html", form=form)


@app.route("/edit_dog/<int:id>", methods=["GET", "POST"])
def edit_dog(id):
    selected_dog = Dog.query.get(id)
    form = AddDogForm(name=selected_dog.name, img=selected_dog.img, description=selected_dog.description)
    print(selected_dog)
    if request.method == "POST":
        file = request.files['img']
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        selected_dog.name = form.name.data
        selected_dog.img = filename
        selected_dog.description = form.description.data
        db.session.commit()
        return redirect("/")
    return render_template("add_dog.html", form=form)

@app.route("/delete_dog/<int:id>", methods=["GET", "POST"])
def delete(id):
    deleted_dog = Dog.query.get(id)
    db.session.delete(deleted_dog)
    db.session.commit()
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if request.method == "POST":
        user = User(username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("თქვენ წარმატებით გაიარეთ რეგისტრაცია")
        return redirect("/")
    return render_template("registration.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LogInForm()
    if request.method == "POST":
        user = User.query.filter(User.username == form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash("თქვენ წარმატებით გაიარეთ ავტორიზაცია")
            return redirect("/")
        else:
            flash("სახელი ან პაროლი არასწორია")
            print("here")
            return redirect ("/login")

    return render_template("login2.html", form=form)

@app.route("/logout", methods=["GET", "POST"])
def logout():
    logout_user()
    flash("თქვენ გამოხვედით საიტიდან")
    return redirect("/")


@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    if query:
        dogs = Dog.query.filter(Dog.name.ilike(f'%{query}%') | Dog.description.ilike(f'%{query}%')).all()
    else:
        dogs = Dog.query.all()
    return render_template('about.html', dogs=dogs)
"""
CRUD - Create Retrieve Update Delete
"""