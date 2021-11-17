import os
import binascii
from flask import *
app = Flask(__name__)

# we will work on tokens

def block_check(token):
    b = open("blacklist_tokens_server.txt", 'r')
    token_block = b.read().split('\n')
    b.close()
    token = str(token)
    for i in token_block:
        tok = i.split(',')[0]
        if token in tok:
            return render_template('block.html')        
    return 0

@app.route('/')
def index():
    token = request.cookies.get('TOKEN')
    status = block_check(token)
    if status!=0:
        return status

    resp = make_response(render_template('index.html'))
    if token == None:
        TOKEN = binascii.hexlify(os.urandom(10)).decode()
        token = TOKEN
        resp.set_cookie('TOKEN', TOKEN)

    f = open("log/server.data","a")
    f.write(token+"     /\n")
    f.close()

    return resp
    


@app.route('/login.html', methods=['GET', 'POST'])
def login():

    token = request.cookies.get('TOKEN')
    if token == None:
        return redirect('/')

    status = block_check(token)
    if status!=0:
        return status

    b = open("blacklist_tokens_login.txt", 'r')
    token_block = b.read().split('\n')
    b.close()
    for i in token_block:
        tok = i.split('\t')[0]
        if token in tok:
            return render_template('block.html')

    f = open("log/server.data","a")
    f.write(token+"     /login.html\n")
    f.close()

    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'

            f = open("log/login.data","a")
            lo = [token,request.form['username'],request.form['password']]
            f.write(lo[0]+"     "+lo[1]+"     "+lo[2]+"\n")
            f.close()

            return render_template('login.html',error=error)
        else:
            return "<h1>You logged in</h1>"
    return render_template('login.html')



@app.route('/signup.html')
def signup():
    token = request.cookies.get('TOKEN')
    if token == None:
        return redirect('/')
    status = block_check(token)
    if status!=0:
        return status
    f = open("log/server.data","a")
    f.write(token+"     /signup.html\n")
    f.close()
    return render_template("signup.html")

if __name__ == '__main__':
    app.run('127.0.0.1', 8080)