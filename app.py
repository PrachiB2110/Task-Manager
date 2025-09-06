from flask import Flask,render_template,request,redirect,session,url_for,flash
from flask_sqlalchemy import SQLAlchemy 

from werkzeug.security import generate_password_hash, check_password_hash
from faceRecog import capture_and_store_face, authenticate_face 

from datetime import datetime

app = Flask(__name__)

import os
#because Heroku doesnt use sqlite

#if hosting local,this works fine - app.config['SQLALCHEMY_DATABASE_URI'] =  'sqlite:///test.db' 

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'sqlite:///test.db'


app.secret_key = 'secret_key'  


db=SQLAlchemy(app)

class Todo(db.Model):
    
    id = db.Column(db.Integer,primary_key=True)
    content = db.Column(db.String(200),nullable=False)
    date_created = db.Column(db.DateTime,default = datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    


    def __repr__(self): 
        return '<Task %r>' % self.id

class User(db.Model):
    user_id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(80),unique=True,nullable=False)
    password = db.Column(db.String(200),nullable=False)
    tasks = db.relationship('Todo', backref='user', lazy=True)    
    def __repr__(self):
        return '<User %r>' % self.username

@app.route('/',methods =['GET','POST'])

def index():
    
    if 'user_id' in session:  # Check if user is logged in
        return redirect(url_for('home', user_id=session['user_id']))  # Redirect to user's home page
    
    return render_template('index.html')

@app.route('/home/<int:user_id>',methods =['GET','POST'])

def home(user_id):
    if 'user_id' not in session or session['user_id'] != user_id:  # Verify user ID in session
        return redirect('/signin/')
    if request.method=='POST':

        task = request.form['content']
        add = Todo(content = task,user_id=user_id)
        try:
            db.session.add(add)
            db.session.commit()
            return redirect(url_for('home',user_id=user_id))
        except:
            return "Unable to add Task"
        

    else:
        tasks = Todo.query.filter_by(user_id=user_id).order_by(Todo.date_created).all()
        return render_template('home.html',tasks = tasks,user=User.query.filter_by(user_id=user_id).first())

@app.route('/delete/<int:id>')

def delete(id):
    task = Todo.query.get_or_404(id)
    try : 
        db.session.delete(task)
        db.session.commit()
        return redirect(url_for('home', user_id=session['user_id']))
    except:
        return "Delete Failed"

@app.route('/update/<int:id>',methods = ['GET','POST'])
def update(id):
    task =Todo.query.get_or_404(id)
    if request.method == 'POST':
        
        try:
            task.content = request.form['content']
            db.session.commit()


            return redirect(url_for('home', user_id=session['user_id']))
        except:
            return "Unable to Update"
        
    else : 
        return render_template('update.html',task =task)
    
@app.route('/signup/',methods = ['GET','POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            
            return redirect('/signin/')
            
            
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new = User(username=username, password=hashed_password)

        try:
            db.session.add(new)
            db.session.commit()
            session['user_id']=new.user_id
            
            capture_and_store_face(username)
            return redirect(url_for('home',user_id=new.user_id))
        except:
            return 'Unable to Add User'
    else:
        return render_template('signup.html')

@app.route('/signin/',methods = ['GET','POST'])
def signin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        existing_user = User.query.filter_by(username=username).first()

        if existing_user and check_password_hash(existing_user.password, password):
            session['user_id'] = existing_user.user_id

            return redirect(url_for('face',id=existing_user.user_id))
        else:
            return redirect('/signin/')
    else:
        return render_template('signin.html')

@app.route('/face/<int:id>')
def face(id):

    if authenticate_face(User.query.filter_by(user_id=id).first().username):
        return redirect(url_for('home',user_id= id))
    else:
      
        flash("Authentication failed! Please try again.")
        return redirect(url_for('signin'))


@app.route('/logout')
def logout():
    session.clear()  
    return redirect('/')
    

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True,port=8080,host='0.0.0.0')