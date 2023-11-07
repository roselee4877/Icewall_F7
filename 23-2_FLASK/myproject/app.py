import os
from flask import Flask, request, render_template, redirect, session, flash, url_for
from models import db, User
from models import Post
app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def hello():
    if 'username' not in session:
        flash('로그인하십시오', '')
        return redirect('/login/')
    else:
        username = session['username']
        flash('hello, {}'.format(username))
        return "Hello, " + username
        #return render_template("home.html")
    
@app.route('/signup/', methods = ['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not(username):
            return "사용자 이름이 입력되지 않았습니다" 
        else:
            usertable = User()
            usertable.username = username
            usertable.password = password

            db.session.add(usertable)
            db.session.commit()
            return redirect('/')      
    else:
        return render_template("signup.html")
    
@app.route('/login/', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

    #print(username) -> 터미널에서 username 확인해 디버깅 가능

        if not(username and password):
            return "입력되지 않은 정보가 있습니다"
        else:
            user = User.query.filter_by(username = username).first()
            if user:
                if user.password == password:
                    session['username'] = username
                    return redirect('/')
                else:
                    return "비밀번호가 다릅니다"
            else:
                return "사용자가 존재하지 않습니다"
    else:
        return render_template('login.html')
    
@app.route('/logout/', methods = ['GET', 'POST'])
def logout():
    session.pop('username', None)
    return redirect('/')

@app.route('/post/', methods = ['GET', 'POST'])
def post():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')

        if not (title and content):
            return "입력되지 않은 정보가 있습니다."
        else:
            posttable = Post()
            posttable.title = title
            posttable.content = content

            db.session.add(posttable)
            db.session.commit()
            return redirect('/post_list')
    else:
        return render_template('post.html')

if __name__ == "__main__":
    with app.app_context():
        basedir = os.path.abspath(os.path.dirname(__file__))
        dbfile = os.path.join(basedir, 'db.sqlite')
        
        app.config['SECRET_KEY'] = "ICEWALL"
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + dbfile
        app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
        app.config['SQLALCHEMY_TACK_MODIFICATIONS'] = False

        db.init_app(app)
        db.app = app
        db.create_all()

        app.run(host = "127.0.0.1", port = 5000, debug = True)

