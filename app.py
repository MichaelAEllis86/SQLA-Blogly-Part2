from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI']='postgresql:///blogly_db'
app.config['SQLALCHEMY_ECHO']= True
app.config['SECRET_KEY']="oh-so-secret"
debug=DebugToolbarExtension(app)

connect_db(app)
# Home/Base Route

@app.route("/")
def show_base():
    """show base/home page"""
    return render_template("base.html")

# User Routes
@app.route("/users")
def show_user_list_page():
    """show all the users in our db"""
    users=User.query.all()
    return render_template("users.html", users=users )

@app.route("/users/new")
def show_new_user_form_page():
    """show the form page to create a new user"""
    return render_template("userform.html")

@app.route("/users/new", methods=['POST'] )
def handle_new_user_form():
    """handle the form page POST route submission to create a new user"""
    first_name=request.form["first_name"]
    last_name=request.form["last_name"]
    image_url=request.form["image_url"]
    print(f"the form data is first name={first_name} last_name={last_name} image url={image_url}")
    new_user=User(first_name=first_name, last_name=last_name, image_url=image_url)
    print(f"the new user is {new_user}")
    db.session.add(new_user)
    db.session.commit()
    flash("new user created!!")
    flash(f"your new user is {new_user.first_name} {new_user.last_name} with a user id of {new_user.id}", "success")
    return redirect("/users")

@app.route("/users/<user_id>")
def show_user_details(user_id):
    """show details about user page and the user's posts"""
    user=User.query.get(user_id)
    print("the user is", user)
    print(f"the user_id is {user_id}")
    print(f"the user_id type is {type(user_id)}")
    user_posts=user.post_info
    return render_template("userdetail.html", user=user, user_id=user_id, user_posts=user_posts)

@app.route("/users/<user_id>/edit")
def show_user_edit(user_id):
    """Show form page to edit an existing user"""
    user=User.query.get(user_id)
    return render_template("usereditform.html", user=user,user_id=user_id)

@app.route("/users/<user_id>/edit", methods=['POST'])
def handle_user_edit(user_id):
    """handle the user edit post form submission to edit a user"""
    first_name=request.form["first_name"]
    last_name=request.form["last_name"]
    image_url=request.form["image_url"]
    user=User.query.get(int(user_id))
    print(f"this is the intial user{user}")
    user.first_name=first_name
    user.last_name=last_name
    user.image_url=image_url
    print(f"this is user now {user}")
    db.session.add(user)
    db.session.commit()
    flash("user edited!!")
    flash(f"your user is now {user.first_name}{user.last_name} with a user id of {user.id}", "success")
    return redirect("/users")

@app.route("/users/<user_id>/delete", methods=['POST'])
def handle_user_delete(user_id):
    print(f" the initial user_id is {user_id} and it's type is {type(user_id)}")
    integer_user_id=int(user_id)
    user=User.query.get(int(user_id))
    User.query.filter_by(id=integer_user_id).delete()
    db.session.commit()
    flash("user deleted!!")
    flash(f"the previous user of {user.first_name}{user.last_name} with a user id of {user.id} is now deleted", "success")
    return redirect("/users")

# Routes to d0/ Post routes

@app.route("/users/<user_id>/posts/new")
def show_new_post_form_page(user_id):
    user=User.query.get(int(user_id))
    integer_user_id=int(user_id)
    return render_template("newpostform.html", user=user, integer_user_id=integer_user_id)

@app.route("/users/<user_id>/posts/new", methods=['POST'])
def handle_new_post_form_page(user_id):
    integer_user_id=int(user_id)
    post_title=request.form['title']
    post_content=request.form['content']
    print(f"the form data is post_title={post_title} post_content={post_content}")
    new_post=Post(title=post_title, content=post_content, user_id=int(user_id))
    db.session.add(new_post)
    db.session.commit()
    flash("new post created!!")
    flash(f"your new post is {new_post.title}, created by {new_post.user_info.first_name} {new_post.user_info.last_name} at {new_post.created_at}", "success")
    return redirect (f"/users/{integer_user_id}")

@app.route("/posts/<post_id>")
def show_post(post_id):
    integer_post_id=int(post_id)
    post=Post.query.get(integer_post_id)
    integer_user_id=int(post.user_info.id)
    return render_template("showpost.html", post=post, integer_user_id=integer_user_id)

@app.route("/posts/<post_id>/edit")
def show_edit_post_form_page(post_id):
    integer_post_id=int(post_id)
    post=Post.query.get(integer_post_id)
    integer_user_id=int(post.user_info.id)
    return render_template("posteditform.html", post=post, integer_user_id=integer_user_id)

@app.route("/posts/<post_id>/delete", methods=['POST'])
def handle_post_deletion(post_id):
    integer_post_id=int(post_id)
    post=Post.query.get(integer_post_id)
    Post.query.filter_by(id=integer_post_id).delete()
    db.session.commit()
    flash("Post deleted!!", "success")
    # flash(f"the previous post {post.title} by {post.user_info.first_name} is now deleted" "success")----->seems like this flash msg isnt working because the post cannot be referenced once deleted?
    return redirect("/users")

@app.route("/posts/<post_id>/edit", methods=['POST'])
def handle_edit_post_edit(post_id):
    integer_post_id=int(post_id)
    post_title=request.form["title"]
    post_content=request.form["content"]
    print(f"the form data is post_title={post_title} post_content={post_content}")
    post=Post.query.get(integer_post_id)
    post.title=post_title
    post.content=post_content
    db.session.add(post)
    db.session.commit()
    integer_user_id=int(post.user_info.id)
    flash("Post Edited!!", "success")
    return redirect (f"/posts/{integer_post_id}")
    
# to do!!!!!
# further study for part 2
