from flask import Flask,render_template,request,redirect,url_for
import sqlite3
import os
from werkzeug.utils import secure_filename
app=Flask(__name__)
UPLOAD_FOLDER="static/upload"
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER
@app.route('/')
def index():
    return render_template('registerform.html')
@app.route('/register',methods=['POST'])
def register():
    if request.method=="POST":
        name=request.form['name']
        mobile=request.form['mobile']
        gender=request.form.getlist('gender')
        dob=request.form['date']
        course=request.form['course']
        lang = request.form.getlist('lang')
        l=""
        for i in lang:
            if i!="":
                l=l+","+i
        addr=request.form['address']
        file=request.files['file']
        file1=secure_filename(file.filename)
        print(type(file))
        print(type(name))
        print(type(mobile))
        print(type(gender))
        print(type(dob),type(course),type(lang),type(addr),type(file1))


        file.save(os.path.join(app.config['UPLOAD_FOLDER'],file1))
        conn=sqlite3.connect("user.db")
        conn.execute("INSERT INTO student(name,mob,gender,dob,course,languages,address,profile)VALUES(?,?,?,?,?,?,?,?)",(name,mobile,gender[0],dob,course,l,addr,file1))
        conn.commit()
        msg = "Registration Done"
        return render_template('registerform.html',msg=msg)
@app.route('/view')
def view():
    conn=sqlite3.connect('user.db')
    cur=conn.execute("SELECT * FROM student")
    rows=cur.fetchall()
    return render_template('view.html',rows=rows)
@app.route('/edit/<a>')
def edit(a):
    conn=sqlite3.connect('user.db')
    cur=conn.execute("SELECT * FROM student WHERE id=?",(a,))
    row=cur.fetchone()
    return render_template('edit.html',row=row)

@app.route('/update/<a>',methods=['POST'])
def update(a):
    if request.method == "POST":
        name = request.form['name']
        mobile = request.form['mobile']
        gender = request.form.getlist('gender')
        dob = request.form['date']
        course = request.form['course']
        lang = request.form.getlist('lang')
        l = ""
        for i in lang:
            if i != "":
                l = l + "," + i
        addr = request.form['address']


        conn = sqlite3.connect("user.db")
        conn.execute("UPDATE student SET name=?,mob=?,gender=?,dob=?,course=?,languages=?,address=? WHERE id=?",
                     (name, mobile, gender[0], dob,  course,l, addr,a))
        conn.commit()

        return redirect(url_for('view'))
@app.route('/delete/<a>')
def delete(a):
    conn=sqlite3.connect('user.db')
    conn.execute("DELETE FROM student WHERE id=?",(a,))
    conn.commit()
    return redirect(url_for('view'))
if __name__=="__main__":
    app.run(debug=True)