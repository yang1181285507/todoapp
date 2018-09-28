from flask import Flask,request, render_template,redirect
import datetime,pymysql

app = Flask(__name__)

def get_connection():
    cn =pymysql.connect(host='127.0.0.1', user='root', password='root', db='my-test')
    return cn

def add_new_task(content):
    cn = get_connection()
    try:
        cs = cn.cursor()
        cs.execute("insert into manage(task) values(%s)",(content,))
        cn.commit()
    finally:
        cn.close()

def delete_task(com):
    cn=get_connection()
    try:
        cs=cn.cursor()
        cs.execute("delete from manage where id=%s",(com,))
        cn.commit()
        return cs.fetchall()
    finally:
        cn.close()

def delete_completed_task():
    cn=get_connection()
    try:
        cs=cn.cursor()
        cs.execute("delete from manage where complete=0")
        cn.commit()
        return cs.fetchall()
    finally:
        cn.close()

def get_completed(cc):
    cn = get_connection()
    try:
        cs = cn.cursor()
        cs.execute("update manage set complete='0' where id=%s",(cc,))
        cn.commit()
        return cs.fetchone()
    finally:
        cn.close()

def get_complete(dd):
    cn = get_connection()
    try:
        cs = cn.cursor()
        cs.execute("update manage set complete='1' where id=%s",(dd,))
        cn.commit()
        return cs.fetchone()
    finally:
        cn.close()

def cha_task_complete(ee):
    cn = get_connection()
    try:
        cs = cn.cursor()
        cs.execute("select complete from manage where id=%s",(ee,))
        return cs.fetchone()
    finally:
        cn.close()

def cha_uncomplete_task():
    cn=get_connection()
    try:
        cs=cn.cursor()
        cs.execute("select * from manage where complete=0")
        cn.commit()
        return cs.fetchall()
    finally:
        cn.close()

def cha_complete_task():
    cn=get_connection()
    try:
        cs=cn.cursor()
        cs.execute("select * from manage where complete=1")
        cn.commit()
        return cs.fetchall()
    finally:
        cn.close()

def get_history_tasks():
    cn = get_connection()
    try:
        cs = cn.cursor()
        cs.execute("select * from manage order by id asc limit 10")
        return cs.fetchall()
    finally:
        cn.close()

def add_new_log(username,password):
    cn = get_connection()
    try:
        cs = cn.cursor()
        cs.execute(f"insert into log(username,password) values('{username}','{password}')")
        cn.commit()
    finally:
        cn.close()

def cha_log(name):
    cn = get_connection()
    try:
        cs = cn.cursor()
        cs.execute(f"select password from log where username=('{name}')")
        return cs.fetchone()
    finally:
        cn.close()

def update_task(t,d):
    cn = get_connection()
    try:
        cs = cn.cursor()
        cs.execute("update manage set task=%s  where  id=%s",(t,d,))
        cn.commit()
        return cs.fetchone()
    finally:
        cn.close()


@app.route('/')
def index():
    return render_template('login_table.html')


@app.route('/registers')
def registers_notes():
    return render_template('register.html')


@app.route('/submit',methods=['POST','GET'])
def submit_notes():
    if request.method=='GET':
        notes_username = request.args.get('username')
        na=notes_username.islower()
        notes_pwd1 = request.args.get('pwd1')
        notes_pwd2= request.args.get('pwd2')
        if na==True:
            if notes_pwd1 is not None:
                if notes_pwd2==notes_pwd1:
                    add_new_log(notes_username,notes_pwd1)
                    return redirect('/')
                else:
                    return '注册失败. <a href="/registers">返回</a>'
            else:
                return '注册失败. <a href="/registers">返回</a>'
        else:
            return '用户名长度必须为五个字符，注册失败. <a href="/registers">返回</a>'
    else:
        username = request.form.get('name')
        pwd=request.form.get('pwd')
        shuju_pwd=cha_log(username)
        if shuju_pwd is not None:
            if pwd==shuju_pwd[0]:
                return redirect('/task')
            else:
                return '登录失败. <a href="/">返回</a>'
        else:
            return '登录失败. <a href="/">返回</a>'


@app.route('/all')
@app.route('/task')
def task():
    tasks=get_history_tasks()
    return render_template('index.html',tasks=tasks)


@app.route('/new_task')
def new_task():
    shuchu=request.args.get('shuchu')
    add_new_task(shuchu)
    return redirect('/task')


@app.route('/delete')
def delete_one():
    id=request.args.get('id')
    print('id=',id)
    delete_task(id)
    return redirect('/task')


@app.route('/stamp')
def stamp():
    id=request.args.get('id')
    print('id=',id)
    comp=cha_task_complete(id)[0]
    print('comp=',comp)
    if comp==0:
        get_complete(id)
    elif comp==1:
        get_completed(id)
    return redirect('/task')


@app.route('/button')
def delete_completed():
    delete_completed_task()
    return redirect('/task')


@app.route('/completed')
def cha_completed():
    cha_complete_task()
    tasks=cha_uncomplete_task()
    return render_template('index.html', tasks=tasks)


@app.route('/active')
def cha_actived():
    cha_uncomplete_task()
    tasks=cha_complete_task()
    return render_template('index.html', tasks=tasks)


@app.route('/update')
def eidt_task():
    id=request.args.get('id')
    ta=request.args.get('content')
    print(ta)
    a=update_task(ta,id)
    print('a=',a)
    return redirect('/task')


if __name__ == '__main__':
    app.run(debug=True)