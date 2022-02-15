from flask import Flask, Markup, render_template, request, redirect, flash, session

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_required, login_user, logout_user

from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import pytz
import os
import logging

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///memollection.db'
app.config['SECRET_KEY'] = os.urandom(24)
db = SQLAlchemy(app)
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')
app.permanent_session_lifetime = timedelta(minutes=30)

login_manager = LoginManager()
login_manager.init_app(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post = db.Column(db.String(400), nullable=False)
    post_at = db.Column(db.DateTime, nullable=False, default=datetime.now(pytz.timezone('Asia/Tokyo')))
    author = db.Column(db.String(30))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False, unique=True)
    password = db.Column(db.String(50))

# ログイン機能を使うために必要なコールバック関数
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ログインしていないときはログインページに飛ばす
@login_manager.unauthorized_handler
def unauthorized():
    return redirect('/login')

@app.route("/", methods=['GET', 'POST'])
@login_required
def index():
    body = request.form.get('body')
    if request.method == 'POST' and body != '' :
        atcl = Post(post = body, post_at = datetime.now(pytz.timezone('Asia/Tokyo')), author = session["user"])
        
        db.session.add(atcl)
        db.session.commit()
        
        return redirect('/')

    else :
        past_posts = Post.query.filter(Post.author==session["user"]).all()
        posts_list = []
        date_list = []
        now = datetime.now()
        
        for i, past_post in enumerate(past_posts) :
            date = past_post.post_at.strftime('%Y/%m/%d')
            time = past_post.post_at.strftime('%H:%M')
            
            p = past_post.post
            p = p.replace('<', '&lt;')
            p = p.replace('>', '&gt;')
            p = Markup(p.replace('\r', '<br>'))

            if date == now.strftime('%Y/%m/%d'):
                box_side = 'right_box'
            else :
                box_side = 'left_box'

            if date not in date_list :
                date_list.append(date)
                posts_list.append([past_post.id, box_side, p, time, date])
            else :
                posts_list.append([past_post.id, box_side, p, time, None])

            if past_post.post_at - timedelta(minutes=3) < past_posts[i-1].post_at and i != 0:
                posts_list[i-1][3] = None

        return render_template('index.html', past_posts = posts_list)
    
@app.route("/login", methods=['GET', 'POST'])
def login():
    logout_user()
    if request.method == 'POST':
        username = request.form.get('username')
        pw = request.form.get('pw')
        
        try:
            user = User.query.filter_by(username=username).first()
            if check_password_hash(user.password, pw):
                login_user(user)
                session.permanent = True
                session["user"] = username #sessionにuser情報を保存
                return redirect('/')
            else :
                flash('Incorrect password.')
            return redirect('/login')
        except :
            flash('Incorrect username.')
            return redirect('/login')
    else:
        return render_template('login.html')


@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        pw = request.form.get('pw')
        
        if username != '' and pw != '' :
            user = User.query.filter_by(username=username).first()
        
            if user :
                flash('this username already exists.')
                return redirect('/signup')
            
            user = User(username=username, password=generate_password_hash(pw, method='sha256'))
            
            db.session.add(user)
            db.session.commit()
        
            return redirect('/login')
        else :
            flash('please setting username and password.')
            return redirect('/signup')
            
    else:
        return render_template('signup.html')

    
@app.route("/404")
def notfound():
    return render_template('404.html')


@app.route("/<int:id>/delete")
@login_required
def delete(id):
    post = Post.query.get(id)
    
    db.session.delete(post)
    db.session.commit()
    
    return redirect('/')

@app.route("/<int:id>/edit", methods=['GET', 'POST'])
@login_required
def edit(id):
    body = request.form.get('body')
    if body != '':
        post = Post.query.get(id)
        post.post = body
        
        db.session.commit()
    
    return redirect('/')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop("user", None) #削除
    return redirect('/login')


@app.route("/account_clear", methods=['GET'])
@login_required
def clear():
    user = db.session.query(User)
    for row in user:
        print(row.id, row.username)
    
    id = input()
    try :
        user = User.query.get(id)

        db.session.delete(user)
        db.session.commit()
    except :
        logging.debug('sqlalchemy.orm.exc.UnmappedInstanceError')
  
    return redirect('/')

if __name__ == "__main__":
      app.run(debug=True)