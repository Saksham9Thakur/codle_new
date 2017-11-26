from flask import render_template, request,flash, redirect, url_for,session
from app import app, db
from app.models import *
import datetime 
import os,time
from itertools import cycle
from app.a import *
from app.models import *
from functools import wraps
import requests
from werkzeug import secure_filename
COMPILE_URL = u'http://api.hackerearth.com/code/compile/'
CLIENT_SECRET = '83988f98843586056cd399a7e1cfe9f1b4e0e6e9'
app.config['UPLOAD_FOLDER']='/home/saksham/codle12/'
def login_required(f):
	@wraps(f)
	def wrap(*args,**kwargs):
		if 'logged_in' in session:
			return f(*args,**kwargs)
		else:
			flash('You need to login first')
			return redirect(request.referrer)
	return wrap

def login_required2(f):
	@wraps(f)
	def wrap(*args,**kwargs):
		a=datetime.datetime.now()
		b=Contest.query.filter_by(name=session["contest"]).first()
		if 'logged_in' in session:
			if(a<b.end_time):
				return f(*args,**kwargs)
			else:
				flash('Contest over')
				return redirect(request.referrer)	
		else:
			flash('You need to login first as admin')
			return redirect(request.referrer)
	return wrap
def login_required_admin(f):
	@wraps(f)
	def wrap(*args,**kwargs):
		if 'logged_in_ad' in session:
			return f(*args,**kwargs)
		else:
			flash('You need to login first')
			return redirect(request.referrer)
	return wrap
@app.errorhandler(404)
def page_not_found(e):
    return render_template('page-404.html')
@app.errorhandler(500)
def page_not_found(e):
	flash("You are doing an invalid step")
	return render_template('page-500.html')
@app.route('/' )
def index():
  return render_template('welcome.html') 

@app.route('/userinfo' )
@login_required
def inde():
	a=Leaderboard.query.filter_by(username=session['username']).first()
	us=a.username
	em=a.email
	po=a.score
	return render_template("page-blank.html",name=us,email=em,score=po)
  
@app.route('/register',methods=['POST','GET'])
def reg():
	if request.method=="POST":
		user = Leaderboard.query.filter_by(username=request.form['username']).first()
		print user
		if user==None:
			if(request.form['password'] ==request.form['password-check']):
				a=Leaderboard(request.form['username'],request.form['email'],0,request.form['password'])
				db.session.add(a)
				db.session.commit()
				return redirect(url_for('index'))
			else:	
				flash("Passwords do not match")
		else:
			flash("Username already exists")	
	return render_template('page-register.html')		


@app.route("/admin")
@login_required_admin
def admin():
	return render_template("admin_view.html")

@app.route("/addcontest",methods=["POST"])
@login_required_admin
def addcon():
	name=request.form['name']
	start_time=request.form['start_time']
	end_time=request.form['end_time']
	b=Contest.query.all()
	q=0
	for m in b:
		if(m.name==name):
			flash('Name cannot repeat')
			q=1
	if(q==1):
		return redirect(url_for('admin'))		
	else:	
		p=0
		a=Contest(name,start_time,end_time)
		db.session.add(a)
		db.session.commit()
		if( a.start_time>datetime.datetime.now()  and a.start_time<a.end_time ):
			flash('End time cannot be greater than start time')
		else:
			p=1
		for i in b:
			if((i.start_time<a.start_time and i.end_time<a.start_time) or (i.start_time>a.start_time and i.start_time>a.end_time)):			
				pass
			else:
				flash('Timings of two events cannot overlap')
				p=1
				break
		if(p==0):	 
			##insert logic of time.start time should be more than current and so on..
			print 'contest has been added'
			session['UPLOAD_FOLDER']=app.config['UPLOAD_FOLDER']+name
			os.makedirs(session['UPLOAD_FOLDER'])
			os.makedirs(session['UPLOAD_FOLDER']+"/questions")
			os.makedirs(session['UPLOAD_FOLDER']+"/answers")
			os.makedirs(session['UPLOAD_FOLDER']+"/tests")
			os.makedirs(session['UPLOAD_FOLDER']+"/editorial")
		else:
			print 'deleting pop'
			db.session.delete(a)
			db.session.commit()
			return redirect(url_for('admin'))
	return redirect(url_for('addquestion'))

@app.route("/addque")
@login_required_admin
def addquestion():
	return render_template("question_add.html",ia=(session["ia"]%4))

@app.route('/uploader', methods = ['GET', 'POST'])
@login_required_admin
def upload():
	if request.method == 'POST':
		uploaded_files = request.files.getlist("file[]")
	   	for file in uploaded_files:
		   	filename = secure_filename(file.filename)
		   	print session['UPLOAD_FOLDER'],filename
		   	if(filename==''):
		   		print 'file ni ayi koi'
		   		pass
		   	else:
		   		if(session["ia"]%4==0):
				   	file.save(os.path.join(session['UPLOAD_FOLDER']+"/questions", filename))
				   	session["question"]=filename
				   	session["question_name"]=request.form["name"]
				   	session["marks"]=request.form["marks"]
				   	print filename,"is question"
				if(session["ia"]%4==1):
				   	file.save(os.path.join(session['UPLOAD_FOLDER']+"/answers", filename))
				   	session["answers"]=filename
				   	print filename,"is answer"
				if(session["ia"]%4==2):
				   	file.save(os.path.join(session['UPLOAD_FOLDER']+"/tests", filename))   	   	
				   	session["test"]=filename
				   	session["editorial"]=filename
				   	print filename,"is answer"   	
				if(session["ia"]%4==3):
				   	file.save(os.path.join(session['UPLOAD_FOLDER']+"/editorial", filename))   	   	
				   	session["editorial"]=filename
					#print 'the value of test is answer',answers 	
				   	a=0
				   	b=0
				   	s=''
				   	for i in os.path.join(session['UPLOAD_FOLDER']):
				   		if(a>=4):
				   			s=s+i
				   		if(i=='/'):
				   			a+=1
				  	#s='p'""	
				  	#print "The name is %s"%s
				  	print s
				   	cona = Contest.query.filter_by(name=s).first()
			   		m=cona.question
			   		p=0
			   		for i in m:
			   			if(i.question_name==session["question"] or i.ans_name==session["question"] or i.test_name==session["question"] ):
			   				p=1
			   				break

			   		if(p==1):
			   			print 'File has already been added'
			   			break
					if(p!=1 and session["ia"]%4==3):   	
						#print 'the value of test is answer',answers	
				   		a=Questions(session["question"],session["marks"],session["answers"],session["test"],cona,session["editorial"])
				   		db.session.add(a)
						db.session.commit()	
					   	m=open(session['UPLOAD_FOLDER']+'/info.txt','a')
					   	print 'file has been uploaded'
					   	print 'file has been uploaded'
						aa=session["question_name"]+'\n'
						m.write(aa)	
						m.write(session["question"]+'\n')
						m.close()	
						print 'file has been uploaded'
	session["ia"]+=1				
	return redirect(url_for('addquestion'))

@app.route("/score")
@login_required
def score():
	b=Leaderboard.query.order_by(Leaderboard.score.desc()).all()
	return render_template("score.html",b=b)

@app.route("/scores")
@login_required_admin
def scores():
	b=Leaderboard.query.order_by(Leaderboard.score.desc()).all()
	return render_template("score.html",b=b)

@app.route("/contest")
@login_required_admin
def cont():
	b=Contest.query.all()
	return render_template("page-blank1.html",b=b)

@app.route("/contests")
@login_required
def conts():
	b=Contest.query.all()
	return render_template("page-blank1.html",b=b)

@app.route("/afterlogin")
@login_required
def afte():
	a=datetime.datetime.now()
	b=Contest.query.all()
	c=a
	d=''
	flag=0
	for i in b:
		if(i.end_time>a and i.start_time<a):#and i.start_time<a
			c=i.end_time
			d=i.name
			session["contest"]=d
			flag=1
	if(d==''):		
		for i in b:
			if(i.start_time>a):
				c=i.start_time
				d=i.name
				session["contest"]=d
				flag=2
	print 'ta is',app.config['UPLOAD_FOLDER']				
	session['UPLOAD_FOLDER']=app.config['UPLOAD_FOLDER']+d
	if(d==''):
		d='No contest available'
	t=0	
	if(flag==2 or flag==1):
		c=c-a
		f=divmod(c.days * 86400 + c.seconds, 60)
		p=0
		print f,"aya"
		for x in range(len(f)-1,-1,-1):
			print f[x],"is value"
		for x in xrange(1,-1,-1):
			print f[x],'aya'
			if(p==0):
				t+=f[x]
			elif(p==1):
				t+=f[x]*60
			elif(p==2):
				t+=f[x]*60*60*24		
			p+=1
	print t,flag
	return render_template("afteruserlogin.html",Name=session["username"],d=d,flag=flag,t=t)

@app.route('/login',methods=['POST','GET'])
def login():
	if request.method=="POST":
		session["ia"]=0
		session["answers"]=''
		session["editorial"]=''
		session["question"]=''
		session["test"]=''
		session["question_name"]=''
		session["marks"]=0
		session["username"]=''
		if(request.form['username']=='admin' and request.form['password']=='admin' ):
			session['logged_in_ad'] = True
			session["username"]='admin'
			session['UPLOAD_FOLDER']=app.config['UPLOAD_FOLDER']
			return redirect(url_for('admin'))
		user = Leaderboard.query.filter_by(username=request.form['username']).first()
	#	print user
		if user == None:
			flash("You are not registered")
		else:
			if bcrypt.check_password_hash(user.password, request.form['password']) == False:
				flash('Password is wrong')
			else:
				session["username"]=request.form['username']
				session['logged_in'] = True
				flash('Logged in successfully')
				return redirect(url_for("afte"))
	return render_template('page-login.html')    

@app.route('/showquestion')
@login_required
def sho():
	a=open(session['UPLOAD_FOLDER']+'/info.txt','r')
	dic={}
	b=a.readline()
	while(b):
		c=a.readline()
		dic[b]=c
		b=a.readline()
		print dic
	print dic	
	session["code"]=""
	session["error"]=""
	session["lang"]=""
	print session["contest"]
	return render_template("question.html",a=dic,b=session["contest"])
@app.route('/show/<ques>')
@login_required2
def qow(ques):
	c=Questions.query.filter_by(question_name=ques).first()
	f = open(session['UPLOAD_FOLDER']+'/questions/'+ques)
	Statement=''
	INPUTS=''
	OUTPUTS=''
	CONSTRAINTS=''
	m=0
	for i in f:
		if(i=='Input\n' or i=='Output\n' or i=='Constraints\n'  ):
			m+=1
		if(m==0 and i!='Statement\n'):
			Statement+=i
		if(m==1 and i!='Input\n'):
			INPUTS+=i
		if(m==2 and i!='Output\n'):
			OUTPUTS+=i
		if(m==3 and i!='Constraints\n'):
			CONSTRAINTS+=i
	f.close()	
	Statement = unicode(Statement, 'utf-8')
	INPUTS = unicode(INPUTS, 'utf-8')
	OUTPUTS = unicode(OUTPUTS, 'utf-8')
	CONSTRAINTS = unicode(CONSTRAINTS, 'utf-8')
	return render_template("question_page.html",code=session["code"],Statement=Statement,Inputs=INPUTS,Outputs=OUTPUTS,Constraints=CONSTRAINTS,ques=ques,error=session['error'],marks=c.marks)

@app.route("/compile",methods=['POST','GET'])
@login_required2
def runn():
	lang=request.form["val"]
	print type(lang),"is the type of language"
	code=request.form["value"]
	if(lang=="1"):
		lang="C"
	if(lang=="2"):
		lang="CPP"
	if(lang=="3"):
		lang="JAVA"
	if(lang=="4"):
		lang="PYTHON"			
	#use this to compile code
	data = {
    'client_secret': CLIENT_SECRET,
    'async': 0,
    'source': code,
    'lang': lang,
    'time_limit': 5,
    'memory_limit': 262144,
	}
	r = requests.post(COMPILE_URL,data=data)
	a=r.json()
	print a
	print a["message"],"is message"
	print a["compile_status"],"is status",lang,"is language"
	session["error"]=a["compile_status"]
	session["code"]=code
	return redirect(url_for('qow',ques=request.form["question"]))

@app.route("/run",methods=['POST','GET'])
@login_required2
def  runi():
	lang=request.form["val"]
	lan=""
	code=request.form["value"]
	if(lang=="1"):
		lang=".c"
		lan="c"
	if(lang=="2"):
		lang=".cpp"
		lan="cpp"
	if(lang=="3"):
		lang=".java"
		lan="java"
	if(lang=="4"):
		lang=".py"
		lan="python"		
	sa="code"+lang
	fil=open(sa,'w')
	fil.write(code)
	fil.close()
	c=Questions.query.filter_by(question_name=request.form['question']).first()
	fil1=open("testin.txt","w")
	fil2=open(session["UPLOAD_FOLDER"]+"/tests/"+c.test_name)
	for line in fil2.readlines():
		fil1.write(line)
	fil1.close()
	fil2.close()	
	c=Questions.query.filter_by(question_name=request.form['question']).first()
	fil1=open("testout.txt","w")
	fil2=open(session["UPLOAD_FOLDER"]+"/answers/"+c.ans_name)
	for line in fil2.readlines():
		fil1.write(line)
	fil1.close()
	fil2.close()
	codes = {200:'success',404:'file not found',400:'error',408:'timeout'}
	testout = 'testout.txt'
	timeout = '1'
	testin="testin.txt"
	print(codes[compile(sa,lan)])
	print (codes[run('code',testin,timeout,lan,lang)])
	print "Yhan tak to chala"
	if(match(testout)==True):
		mar=c.marks
		print "I worked"
		ca=Leaderboard.query.filter_by(username=session['username']).first()
		pa=ca.solved
		count=0
		for i in pa:
			if(i.id==c.id):
				flash("You have already solved this question")
				count=1
				break
		if(count==0):
			print "score added"		
			ca.score+=mar
			db.session.add(solved(c.id,ca))
			flash("Question successfully solved")
			db.session.commit()
	else:
		flash("wrong answer")
	session["error"]=""
	session["code"]=code
	os.remove("testin.txt")
	os.remove("testout.txt")
	os.remove("out.txt")
	os.remove("code"+lang)
	return redirect(url_for('qow',ques=request.form["question"]))	

@app.route('/logout',methods=['POST','GET'])
def logout():
	session.pop('logged_in', None)
	session.pop('logged_in_ad', None)
	session.pop('ia', None)
	session.pop('answers', None)
	session.pop('contest', None)
	session.pop('question', None)
	session.pop('test', None)
	session.pop('question_name', None)
	session.pop('marks', None)
	session.pop('UPLOAD_FOLDER', None)
	session.pop('editorial', None)
	session.pop('username', None)
	flash("You have successfully logged out")
	return redirect(url_for("index"))
