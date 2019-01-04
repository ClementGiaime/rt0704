# -*- coding:utf-8 -*-
from flask import Flask, session, redirect, url_for, escape, request, render_template
from globalfunction import *

app = Flask(__name__)

# Set the secret key to some random bytes.
app.secret_key = 'J84z0UH06f8gy*fg8vHg'




@app.route('/')
def index():
    #####==========================================================####
    ###   Si le client possède une session redirection vers /home   ###
    if session_is_define() == True :
        return redirect(url_for('home'))
    #####====================####
    ###   Sinon vers /loginb  ###
    elif session_is_define() == False :
        return redirect(url_for('login'))



@app.route('/login', methods=['GET', 'POST'])
def login():
    #####=========================================================####
    ###   Si le client possède une session redirection vers /home  ###
    if session_is_define() == True :
        return redirect(url_for('home'))
    #####===================================================#####
    ###   Si la requet http est de type POST                  ###
    ###   Création d'un session si l'utilisateur est valide   ###
    if request.method == 'POST':
        ## Whitelist
        if string_match(request.form['username']) == True :

            ## Requet sur le fichier XML
            ## list_info_user = ["nom","formation","grade",["matiere1","matiere2"...,"matieren"] ]
            ## Si l'utiliseur n'existe pas list_info_user = []
            list_info_user = request_session(request.form['username'])

            if not list_info_user :
                return render_template('login/index.html', error="L'utilisateur n'existe pas !")
            else :
                session['username'] = list_info_user[0]
                session['formation'] = list_info_user[1]
                session['grade'] = list_info_user[2]
                session['listmatiere'] = list_info_user[3]

                return redirect(url_for('home'))

        else :
            return render_template('login/index.html', error="Caractère incorrecte !")
    else :
        return render_template('login/index.html')




@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    session.pop('formation', None)
    session.pop('grade', None)
    session.pop('listmatiere', None)
    return redirect(url_for('login'))




@app.route('/home')
def home():
    if session_is_define() == False :
        return redirect(url_for('login'))

    try:
        if request.args["id"] == "" or request.args["id"] == "home":
            active = "home"
        elif request.args["id"] == "list_qcm":
            active = "list_qcm"
        elif request.args["id"] == "correction_qcm":
            active = "correction_qcm"
        elif request.args["id"] == "create_qcm":
            active = "create_qcm"
        else:
            active = "home"
    except KeyError :
        active = "home"

    list_xml = list_dir("./xml/qcm/", r'.*(.xml)$')
    qcm_allow = list_xml_allow("xml/qcm/", list_xml, session['formation'], session['listmatiere'], session['grade'], session['username'])
    qcm_info = list_xml_info("xml/qcm/", qcm_allow, session['formation'], session['listmatiere'])

    if session['grade'] == "etudiant" :
        return render_template('home/index.html', grade="etudiant", user_info=session, varaible=qcm_info, listmatiere=session['listmatiere'], active=active)
    elif session['grade'] == "professeur" :
        return render_template('home/index.html', grade="professeur", user_info=session, varaible=qcm_info, listmatiere=session['listmatiere'], active=active)




@app.route('/config_QCM')
def config_qcm():
    if session_is_define() == False :
        return redirect(url_for('login'))
    return "Page de configuration avant la création du QCM (Nom du QCM, Matiere, Nombre de question)"




@app.route('/create_qcm', methods=['GET', 'POST'])
def create_qcm():
    if session_is_define() == False :
        return redirect(url_for('login'))

    if request.method == 'POST':
        ## Whitelist
        if string_match(request.form['qcm_name'], r'[A-Za-z0-9]+') == True and list_string_match(request.form.getlist('qcm_matiere'), r'[A-Z0-9]+') == True and string_match(request.form['qcm_question'], r'[0-9]{1,2}') == True and string_match(request.form['qcm_answer'], r'[0-9]{1}') == True:
            #print(request.form.getlist('qcm_matiere'))
            return render_template('create_qcm/index.html', name=request.form['qcm_name'], listmatiere=request.form.getlist('qcm_matiere'), number_question=request.form['qcm_question'], number_awswer=request.form['qcm_answer'])
        else:
            return redirect(url_for('home', id="create_qcm"))
    return "Page de création du QCM, ne s'affiche que quand l'on a configurer le QCM"




@app.route('/list_qcm')
def list_qcm():
    if session_is_define() == False :
        return redirect(url_for('index'))

    ## Récupèrer une list
    ## list_xml = [""]
    list_xml = list_dir("./xml/qcm/", r'.*(.xml)$')
    qcm_allow = list_xml_allow("xml/qcm/", list_xml, session['formation'], session['listmatiere'], session['grade'], session['username'])
    qcm_info = list_xml_info("xml/qcm/", qcm_allow, session['formation'], session['listmatiere'])

    return render_template('list_qcm/index.html', varaible=qcm_info)




if __name__ == '__main__':
    app.run(debug=True)
