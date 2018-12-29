# -*- coding:utf-8 -*-
from flask import Flask, session, redirect, url_for, escape, request, render_template
from globalfunction import *

app = Flask(__name__)

# Set the secret key to some random bytes.
app.secret_key = 'J84z0UH06f8gy*fg8vHg'




@app.route('/')
def index():
    if sessionIsDefine() == True :
        return redirect(url_for('home'))
    elif sessionIsDefine() == False :
        return redirect(url_for('login'))



@app.route('/login', methods=['GET', 'POST'])
def login():
    #####========================================####
    ###   Test si le client possède une session   ###
    if sessionIsDefine() == True :
        return redirect(url_for('home'))
    #####==========================================####
    ###   Test si la requet http est de type POST   ###
    if request.method == 'POST':
        if string_match(request.form['username']) == True :

            list_info_user = request_session(request.form['username'])

            if not list_info_user :
                return render_template('login/index.html', error="L'utilisateur n'existe pas !")
            else :
                session['username'] = list_info_user[0]
                session['formation'] = list_info_user[1]
                session['listmatiere'] = list_info_user[2]
                return redirect(url_for('home'))

        else :
            return render_template('login/index.html', error="Caractère incorrecte !")
        #return redirect(url_for('home'))
    else :
        return render_template('login/index.html')




@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    session.pop('formation', None)
    session.pop('listmatiere', None)
    return redirect(url_for('index'))




@app.route('/home')
def home():
    if sessionIsDefine() == False :
        return redirect(url_for('login'))

    list_xml = list_dir("./xml/qcm/", r'(.xml)$')
    qcm_allow = list_xml_allow("xml/qcm/", list_xml, session['formation'], session['listmatiere'])

    print(qcm_allow)
    html="<h1>Welcome !<h1>"
    for xml in qcm_allow:
        html = html + xml + "<br>"
    return html




@app.route('/config_QCM')
def config_qcm():
    if sessionIsDefine() == False :
        return redirect(url_for('login'))
    return "Page de configuration avant la création du QCM (Nom du QCM, Matiere, Nombre de question)"




@app.route('/create_QCM')
def create_qcm():
    if sessionIsDefine() == False :
        return redirect(url_for('login'))
    return "Page de création du QCM, ne s'affiche que quand l'on a configurer le QCM"




@app.route('/list_qcm')
def list_qcm():
    if sessionIsDefine() == False :
        return redirect(url_for('index'))
    return "Page de choix des QCM"




if __name__ == '__main__':
    app.run(debug=True)
