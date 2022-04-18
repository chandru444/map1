from flask import Flask , redirect , render_template, request
from flask import *
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager , UserMixin , login_required ,login_user, logout_user,current_user
from random import randint
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///map.db'
app.config['SECRET_KEY']='619619'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
db = SQLAlchemy(app)
app.config['UPLOAD_FOLDER'] = 'static/upload'
import sqlite3 as sql
import pandas as pd
login_manager = LoginManager()
login_manager.init_app(app)

class Visitor(UserMixin,db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(200))
    mobile = db.Column(db.String(200))
@login_manager.user_loader
def get(id):
    return student.query.get(id)

class student(UserMixin,db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(200))
    Mobile_Number = db.Column(db.String(200))
def std():      
    @login_manager.user_loader
    def get(id):
        return student.query.get(id)
def vis():
    @login_manager.user_loader
    def get(id):
        return Visitor.query.get(id)


@app.route('/',methods=['POST','GET'])
def home():
    if request.method == 'POST':
        std()
        name = request.form['username']
        id_no = request.form['id']
        if (len(name)<4) or (len(id_no)==0):
            print(len(name))
            return render_template('student.html',mess='mess')
        else:
            user = student(name=name,Mobile_Number=id_no)
            print(user)
            db.session.add(user)
            db.session.commit()
            user = student.query.filter_by(name=name).first()
            print(user)
            a = login_user(user)
            print(a)
            con = sql.connect('map.db')
            cur = con.cursor()
             
            data = pd.read_sql_query('select * from student',con)
            print(data)
            con.commit()
            data.to_csv('student.csv',index=False)
            print(a)
            def random_with_N_digits(n):
                range_start = 10**(n-1)
                range_end = (10**n)-1
                return randint(range_start, range_end)
            screat_no=random_with_N_digits(10)
            session['screat'] = screat_no
            import requests
            url = "https://www.fast2sms.com/dev/bulk"
            payload = "sender_id=FSTSMS&message="+str(screat_no)+"&language=english&route=p&numbers="+id_no
            headers = {
            'authorization': "9AzUfvct8Bo3YumXNjgsZqyDQ5ElW4R6h2SCMindI0GFp7KVbw3P8YTr6hyEmk7QatFGU9LDb4BfVnus",
            'Content-Type': "application/x-www-form-urlencoded",
            'Cache-Control': "no-cache",
            }
            response = requests.request("POST", url, data=payload, headers=headers)
            print(response.text)
            return redirect(url_for('otp'))
            
    return render_template('student.html')

@app.route('/visitor_log',methods=['POST','GET'])
def visitor_log():
    if request.method == 'POST':
        vis()
        name = request.form['username']
        mob = request.form['mob']
        
        if (len(name)<4) or (len(mob)==0):
            print(len(name))
            return render_template('visitor.html',mess='mess')
        else:
            user = Visitor(name=name,mobile=mob)
            print(user)
            db.session.add(user)
            db.session.commit()
            user = Visitor.query.filter_by(mobile=mob).first()
            print(user)
            a = login_user(user)
            print(a)
            con = sql.connect('map.db')
            cur = con.cursor()
            
            data = pd.read_sql_query('select * from Visitor',con)
            print('data')
            con.commit()
            data.to_csv('visitor.csv',index=False)
            def random_with_N_digits(n):
                range_start = 10**(n-1)
                range_end = (10**n)-1
                return randint(range_start, range_end)
            screat_no=random_with_N_digits(10)
            session['screat'] = screat_no
            import requests
            url = "https://www.fast2sms.com/dev/bulk"
            payload = "sender_id=FSTSMS&message="+str(screat_no)+"&language=english&route=p&numbers="+mob
            headers = {
            'authorization': "9AzUfvct8Bo3YumXNjgsZqyDQ5ElW4R6h2SCMindI0GFp7KVbw3P8YTr6hyEmk7QatFGU9LDb4BfVnus",
            'Content-Type': "application/x-www-form-urlencoded",
            'Cache-Control': "no-cache",
            }
            response = requests.request("POST", url, data=payload, headers=headers)
            print(response.text)
            return redirect(url_for('otp'))

    return render_template('visitor.html')
@app.route('/otp',methods=['POST','GET'])
# @login_required
def otp():
    screat_no = session['screat']
    
    print(type(screat_no))
    if request.method == 'POST':
        otp = request.form['otp']
        print(type(otp))
        if otp == str(screat_no):
            return redirect(url_for('homepage'))
        else:
            return render_template('otp.html',error='error')



    return render_template('otp.html')
@app.route('/homepage')
@login_required
def homepage():
    return render_template('homepage.html')

@app.route('/main_block')
@login_required
def main_block():
    return render_template('main_block.html')


@app.route('/main_block1/<string:id>',methods=['POST','GET'])
@login_required
def main_block1(id):
    url = ''
    url = 'main_block'+id+'.mp4'
    # return render_template(url)
    video=url
    return render_template('main_block.html',video=video)

@app.route('/admin_block')
@login_required
def admin_block():
    return render_template('admin_block.html')


@app.route('/admin_block1/<string:id>',methods=['POST','GET'])
@login_required
def admin_block1(id):
    url = ''
    url = 'admin_block'+id+'.mp4'
    # return render_template(url)
    video=url
    return render_template('admin_block.html',video=video)

@app.route('/civil_block')
@login_required
def civil_block():
    return render_template('civil_block.html')


@app.route('/civil_block1/<string:id>',methods=['POST','GET'])
@login_required
def civil_block1(id):
    url = ''
    url = 'civil_block'+id+'.mp4'
    # return render_template(url)
    video=url
    return render_template('civil_block.html',video=video)

@app.route('/main_gate')
@login_required
def main_gate():
    return render_template('main_gate.html')


@app.route('/main_gate1/<string:id>',methods=['POST','GET'])
@login_required
def main_gate1(id):
    url = ''
    url = 'main_gate'+id+'.mov'
    # return render_template(url)
    video=url
    return render_template('main_gate.html',video=video)
@app.route('/electronicblock_1')
@login_required
def electronicblock_1():
    return render_template('electronicblock_1.html')


@app.route('/electronicblock_11/<string:id>',methods=['POST','GET'])
@login_required
def electronicblock_11(id):
    url = ''
    url = 'electronicblock_1'+id+'.mp4'
    # return render_template(url)
    video=url
    return render_template('electronicblock_1.html',video=video)

@app.route('/electronic_block_2')
@login_required
def electronic_block_2():
    return render_template('electronic_block_2.html')


@app.route('/electronic_block_21/<string:id>',methods=['POST','GET'])
@login_required
def electronic_block_21(id):
    url = ''
    url = 'electronic_block_21'+id+'.mp4'
    # return render_template(url)
    video=url
    return render_template('electronic_block_2.html',video=video)

@app.route('/mechanical_block')
@login_required
def mechanical_block():
    return render_template('mechanical_block.html')

@app.route('/mechanical_block1/<string:id>',methods=['POST','GET'])
@login_required
def mechanical_block1(id):
    url = ''
    url = 'mechanical_block'+id+'.mp4'
    # return render_template(url)
    video=url
    return render_template('mechanical_block.html',video=video)

@app.route('/ladies_hostel')
@login_required
def ladies_hostel():
    return render_template('ladies_hostel.html')

@app.route('/ladies_hostel1/<string:id>',methods=['POST','GET'])
@login_required
def ladies_hostel1(id):
    url = ''
    url = 'ladies_hostel'+id+'.mp4'
    # return render_template(url)
    video=url
    return render_template('ladies_hostel.html',video=video)

@app.route('/ground_floor')
@login_required
def  ground_floor():
    return render_template('ground_floor.html')

@app.route('/ground_floor1/<string:id>',methods=['POST','GET'])
@login_required
def ground_floor1(id):
    url = ''
    url = 'ground_floor1'+id+'.mp4'
    # return render_template(url)
    video=url
    return render_template('ground_floor.html',video=video)

@app.route('/first_floor')
@login_required
def  first_floor():
    return render_template('first_floor.html')

@app.route('/first_floor1/<string:id>',methods=['POST','GET'])
@login_required
def first_floor1(id):
    url = ''
    url = 'first_floor1'+id+'.mp4'
    # return render_template(url)
    video=url
    return render_template('first_floor.html',video=video)
@app.route('/second_floor')
@login_required
def  second_floor():
    return render_template('second_floor.html')

@app.route('/second_floor1/<string:id>',methods=['POST','GET'])
@login_required
def second_floor1(id):
    url = ''
    url = 'second_floor1'+id+'.mp4'
    # return render_template(url)
    video=url
    return render_template('second_floor.html',video=video)
@app.route('/third_floor')
@login_required
def  third_floor():
    return render_template('third_floor.html')

@app.route('/third_floor1/<string:id>',methods=['POST','GET'])
@login_required
def third_floor1(id):
    url = ''
    url = 'third_floor1'+id+'.mp4'
    # return render_template(url)
    video=url
    return render_template('third_floor.html',video=video)
@app.route('/fourth_floor')
@login_required
def  fourth_floor():
    return render_template('fourth_floor.html')

@app.route('/fourth_floor1/<string:id>',methods=['POST','GET'])
@login_required
def fourth_floor1(id):
    url = ''
    url = 'fourth_floor1'+id+'.mp4'
    # return render_template(url)
    video=url
    return render_template('fourth_floor.html',video=video)

@app.route('/fifth_floor')
@login_required
def  fifth_floor():
    return render_template('fifth_floor.html')

@app.route('/fifth_floor1/<string:id>',methods=['POST','GET'])
@login_required
def fifth_floor1(id):
    url = ''
    url = 'fifth_floor1'+id+'.mp4'
    # return render_template(url)
    video=url
    return render_template('fifth_floor.html',video=video)
if '__main__' == __name__:
    app.run(debug=True)

