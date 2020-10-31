from flask import Flask, escape, session, request, Response, redirect, url_for, render_template, Markup
import hashlib


tablaUsuarios = {'58d89a3ec111def7c167980ec287b907e66b007c': '3043c70c75558cc7137f783ef76756a4df74f5a8', #bwcarty@att.net:barbarous
                 'c152a0f856e4c59202ad825d2db78be86969b1b6': 'd01593a7b3919244b959c893a0db44f8d82f92b7'}

app = Flask(__name__, template_folder='templates')

#Evidentemente esto JAMÁS debería estar subido al repositorio, recordad que esto es un taller!
app.secret_key = b'_5#y2L"Fadsf\t4Q8zx\n\xec]/'

#Esto debería estar en base de datos, pero para ahorrarme tener que preparar la base de datos, pues tiro por aquí
comentarios = [('ZanahoriaLetal', 'Qué bobada! no me interesa'), ('FanDelSalmón', '¿pero qué narices?')]

@app.route("/blobPage")
def blobPage():
    respuesta = render_template("BlogPage.html", comentarios=comentarios)
    return respuesta

@app.route("/")
def defaultHome():
    return redirect(url_for('blobPage'))

@app.route("/validateLogin", methods=['GET', 'POST'])
def validarLogin():
    if request.method == 'POST':
        user = request.form['user']
        password = request.form['pass']

        print("user: <" + user + ">")
        print("pass: <" + password + ">")

        if hashlib.sha1(user.encode('utf8')).hexdigest() in tablaUsuarios.keys():
            if tablaUsuarios[hashlib.sha1(user.encode('utf8')).hexdigest()] == hashlib.sha1(password.encode('utf8')).hexdigest():
                session['logged'] = user
                return showLogin()
    return showLogin(), 403



@app.route("/login.html")
def showLogin():
    if 'logged' in session:
        respuesta = render_template("logged.html", user=session['logged'])
    else:
        respuesta = render_template("login.html")
    return respuesta

@app.route("/logout", methods=['GET', 'POST'])
def logOut():
    session.pop('logged', None)
    return showLogin()

@app.route("/addComment", methods=['POST'])
def addComment():
    if 'logged' in session:
        #A ver, flask por defecto escapa los caracteres peligrosos. He tenido que recurrir al Markup para poder mostrar en qué consiste el XSS.
        comentarios.append((session['logged'],Markup(request.form['comment'])))
        respuesta = blobPage()
    else:
        respuesta = render_template("error.html")
    return respuesta


@app.route("/favicon.ico")
def favIcon():
    return ""

@app.route("/<page>")
def genericPage(page):
    respuesta = render_template(page)
    return respuesta

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5002')

