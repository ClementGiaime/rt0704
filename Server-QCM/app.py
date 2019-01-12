# -*- coding:utf-8 -*-
from flask import Flask, session, redirect, url_for, escape, request, render_template
from globalfunction import *
from conf import *

app = Flask(__name__)

# Set the secret key to some random bytes.
app.secret_key = SECRET_KEY_APP




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



'''
  _                _
 | |    ___   __ _(_)_ __
 | |   / _ \ / _` | | '_ \
 | |__| (_) | (_| | | | | |
 |_____\___/ \__, |_|_| |_|
             |___/
'''
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
        if request.form.get('username') is None:
            return redirect(url_for('login'))

        if string_match(request.form.get('username')) == True :

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



'''
  _                         _
 | | ___   __ _  ___  _   _| |_
 | |/ _ \ / _` |/ _ \| | | | __|
 | | (_) | (_| | (_) | |_| | |_
 |_|\___/ \__, |\___/ \__,_|\__|
          |___/
'''
@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    session.pop('formation', None)
    session.pop('grade', None)
    session.pop('listmatiere', None)
    session.pop('error_create_qcm', None)
    session.pop('error_list_qcm', None)
    return redirect(url_for('login'))


'''
  _
 | |__   ___  _ __ ___   ___
 | '_ \ / _ \| '_ ` _ \ / _ \
 | | | | (_) | | | | | |  __/
 |_| |_|\___/|_| |_| |_|\___|

'''
@app.route('/home')
def home():
    if session_is_define() == False :
        return redirect(url_for('login'))

    ####==================================================================####
    ## Les variable de session sont utilié pour passé des messages d'erreur ##
    try:
        if session['error_create_qcm']:
            error_create_qcm = session['error_create_qcm']
            session.pop('error_create_qcm', None)
    except KeyError :
        error_create_qcm = ""

    try:
        if session['error_list_qcm']:
            error_list_qcm = session['error_list_qcm']
            session.pop('error_list_qcm', None)
    except KeyError :
        error_list_qcm = ""

    ####====================================================####
    ## variable id passé en GET                               ##
    ## Permet d'afficher la bonne page selon la section voulu ##
    ## /home?id=list_qcm --> Afficher la liste des QCM        ##
    if request.args.get('id') == "" or request.args.get('id') == "home" or request.args.get('id') is None:
        active = "home"
    elif request.args.get('id') == "list_qcm":
        active = "list_qcm"
    elif request.args.get('id') == "correction_qcm":
        active = "correction_qcm"
    elif request.args.get('id') == "create_qcm":
        active = "create_qcm"
    else:
        return redirect(url_for('home'))

    list_xml = list_dir(PATH_QCM, r'.*(.xml)$')
    qcm_allow = list_xml_allow(PATH_QCM, list_xml, session['formation'], session['listmatiere'], session['grade'], session['username'])
    qcm_info = list_xml_info(PATH_QCM, qcm_allow, session['formation'], session['listmatiere'])

    if session['grade'] == "etudiant" :
        return render_template('home/index.html', grade="etudiant", user_info=session, varaible=qcm_info, listmatiere=session['listmatiere'], active=active, error_in_form=error_create_qcm, error_list_qcm=error_list_qcm)
    elif session['grade'] == "professeur" :
        return render_template('home/index.html', grade="professeur", listformation=session['formation'].split(","), varaible=qcm_info, listmatiere=session['listmatiere'], active=active, error_in_form=error_create_qcm, error_list_qcm=error_list_qcm)


'''
                      _
   ___ _ __ ___  __ _| |_ ___     __ _  ___ _ __ ___
  / __| '__/ _ \/ _` | __/ _ \   / _` |/ __| '_ ` _ \
 | (__| | |  __/ (_| | ||  __/  | (_| | (__| | | | | |
  \___|_|  \___|\__,_|\__\___|___\__, |\___|_| |_| |_|
                            |_____| |_|
'''
@app.route('/create_qcm', methods=['GET', 'POST'])
def create_qcm():
    if session_is_define() == False:
        return redirect(url_for('login'))

    if request.method == 'POST':

        if request.form.get('qcm_name') is None or request.form.get('qcm_question') is None or request.form.get('qcm_answer') is None:
            return redirect(url_for('home', id="create_qcm"))
        ####==========================================================================================####
        ##  Vérification de chaque champ du formulaire                                                  ##
        ##  Vérifie si la ou les formation et la matiere sont inclu dans les permissions du professeur  ##
        if form_allow(request.form['qcm_name'], request.form.getlist('qcm_formation'), request.form.getlist('qcm_matiere'), request.form['qcm_question'], request.form['qcm_answer']) == False:
            return redirect(url_for('home', id="create_qcm"))

        ####=======================================================================####
        ##  Si il existe un déjà un QCM avec le même nom donné dans le formulaire    ##
        ##  Redirection vers le formulaire de création de qcm avec message d'erreur  ##
        if qcm_name_exist(PATH_QCM, request.form['qcm_name']) == True:
            session['error_create_qcm'] = "* Un QCM possède déja ce nom (" + request.form['qcm_name'] + ")"
            return redirect(url_for('home', id="create_qcm"))

        return render_template('create_qcm/index.html', name=request.form['qcm_name'], matiere=request.form['qcm_matiere'], listformation=",".join(request.form.getlist('qcm_formation')), listquestion=int(request.form['qcm_question']), listawswer=int(request.form['qcm_answer']))

    return redirect(url_for('home'))


'''
             _ _     _       _
 __   ____ _| (_) __| | __ _| |_ ___     __ _  ___ _ __ ___
 \ \ / / _` | | |/ _` |/ _` | __/ _ \   / _` |/ __| '_ ` _ \
  \ V / (_| | | | (_| | (_| | ||  __/  | (_| | (__| | | | | |
   \_/ \__,_|_|_|\__,_|\__,_|\__\___|___\__, |\___|_| |_| |_|
                                   |_____| |_|
'''
@app.route('/validate_qcm', methods=['GET', 'POST'])
def validate_qcm():
    if session_is_define() == False :
        return redirect(url_for('login'))

    if request.method == 'POST':

        if request.form.get('name') is None or request.form.get('formation') is None or request.form.get('number_question') is None or  request.form.get('number_awswer') is None :
            return redirect(url_for('home', id="create_qcm"))
        ####==========================================================================================####
        ##  Vérification de chaque champ du formulaire                                                  ##
        ##  Vérifie si la ou les formation et la matiere sont inclu dans les permissions du professeur  ##
        if form_allow(request.form['name'], request.form['formation'].split(","), request.form.getlist('matiere'), request.form['number_question'], request.form['number_awswer']) == False:
            return redirect(url_for('home', id="create_qcm"))

        ####=======================================================================####
        ##  Si il existe un déjà un QCM avec le même nom donné dan sle formulaire    ##
        ##  Redirection vers le formulaire de création de qcm avec message d'erreur  ##
        if qcm_name_exist(PATH_QCM, request.form['name']) == True:
            session['error_create_qcm'] = "* Un QCM possède déja ce nom (" + request.form['name'] + ")"
            return redirect(url_for('home', id="create_qcm"))

        ## Création du QCM
        ## <QCM>
        qcm = etree.Element('QCM')
        qcm_correction = etree.Element('QCMCorrection')
        ## <nom>Nom du QCM</nom>
        etree.SubElement(qcm, 'nom').text = request.form['name']
        etree.SubElement(qcm_correction, 'nom').text = request.form['name']
        ## <formation>ASR</formation>
        etree.SubElement(qcm, 'formation').text = request.form['formation']
        ## <matiere>RT0701</matiere>
        etree.SubElement(qcm, 'matiere').text = request.form['matiere']
        ## <auteur>FLAUZAC</auteur>
        etree.SubElement(qcm, 'auteur').text = session['username']

        ## <contenu>
        ## </contenu>
        contenu = etree.SubElement(qcm, 'contenu')
        correction = etree.SubElement(qcm_correction, 'correction')

        for number_question in range(1, int(request.form['number_question']) + 1):
            ## <intitule>
            ## Vérification de chaque question
            question = etree.SubElement(contenu, 'question', num=str(number_question))
            form_number_question = "question_" + str(number_question)
            if string_match(request.form[form_number_question], REGEXP_INPUT_QUESTION) == False:
                session['error_create_qcm'] = "* ERREUR - La question numéro " + str(number_question) + " possède un ou des caractères incorrectes"
                return redirect(url_for('home', id="create_qcm"))

            etree.SubElement(question, 'intitule').text = request.form[form_number_question]

            ## <correction>
            ## Vérification de la valeur de bouton radio
            form_value_awswer = form_number_question + "_awswer"
            regexp_value_awswer = "[1-" + str(request.form['number_question']) + "]"
            try:
                if string_match(request.form[form_value_awswer], regexp_value_awswer) == False:
                    session['error_create_qcm'] = "* ERREUR - au moins une réponse par question doit étre validée"
                    return redirect(url_for('home', id="create_qcm"))
            except KeyError :
                session['error_create_qcm'] = "* ERREUR - au moins une réponse par question doit étre validée"
                return redirect(url_for('home', id="create_qcm"))
            etree.SubElement(correction, 'question', num=str(number_question), id=request.form[form_value_awswer])

            ## <reponses>
            reponses = etree.SubElement(question, 'reponses')
            for number_awswer in range(1, int(request.form['number_awswer']) + 1):
                ## Vérification de chaque réponse
                form_number_awswer = "question_" + str(number_question) + "_awswer_" + str(number_awswer)
                if string_match(request.form[form_number_awswer], REGEXP_INPUT_ANSWER) == False:
                    session['error_create_qcm'] = "* ERREUR - La réponse numéro " + str(number_awswer) + " de la question numéro " + str(number_question) + " possède un ou des caractères incorrectes"
                    return redirect(url_for('home', id="create_qcm"))
                etree.SubElement(reponses, 'reponse', id=str(number_awswer)).text = request.form[form_number_awswer]

        document_xml = etree.ElementTree(qcm)
        document_xml_correction = etree.ElementTree(qcm_correction)

        name_of_qcm = PATH_QCM + request.form['name'] + ".xml"
        name_of_qcm_correction = PATH_QCM_CORRECTION + request.form['name'] + ".xml"

        document_xml.write(name_of_qcm)
        document_xml_correction.write(name_of_qcm_correction)

        return redirect(url_for('home', id="list_qcm"))
    return redirect(url_for('home'))




@app.route('/delete_qcm')
def delete_qcm():
    if session_is_define() == False :
        return redirect(url_for('login'))

    ####=====================================================================####
    ##  Vérifie si l'argument ?ref= existe                                     ##
    ##  Si il existe, test si la référence contient des caractères incorrecte  ##
    ##  Vérifie si le QCM peut être utilié par l'utilisateur                   ##
    if ref_qcm_allow(request.args.get('ref')) == False:
        print(session['error_list_qcm'])
        return redirect(url_for('home', id="list_qcm"))

    qcm = request.args['ref'] + ".xml"

    remove_file(PATH_QCM, qcm)
    remove_file(PATH_QCM_CORRECTION, qcm)
    return redirect(url_for('home', id="list_qcm"))




@app.route('/faire_qcm')
def faire_qcm():
    if session_is_define() == False :
        return redirect(url_for('login'))

    ####=====================================================================####
    ##  Vérifie si l'argument ?ref= existe                                     ##
    ##  Si il existe, test si la référence contient des caractères incorrecte  ##
    ##  Vérifie si le QCM peut être utilié par l'utilisateur  ##
    if ref_qcm_allow(request.args.get('ref')) == False:
        return redirect(url_for('home', id="list_qcm"))

    qcm = request.args['ref'] + ".xml"
    ## List = [ [ ["number","Question 1"],[ ["number","Réponse 1" ], ["number","Réponse 2" ] ] ],
    ##        [ [ ["number","Question 2"],[ ["number","Réponse 1" ], ["number","Réponse 2" ] ] ] ]
    list_question_anwser = qcm_list_question_anwser(PATH_QCM, qcm)
    return render_template('faire_qcm/index.html', list=list_question_anwser, name_qcm=request.args['ref'])
    return redirect(url_for('home', id="list_qcm"))


@app.route('/correction_qcm', methods=['GET', 'POST'])
def correction_qcm():
    if session_is_define() == False :
        return redirect(url_for('login'))

    if request.method == 'POST':
        ####=====================================================================####
        ##  Vérifie si l'argument ?ref= existe                                     ##
        ##  Si il existe, test si la référence contient des caractères incorrecte  ##
        ##  Vérifie si le QCM peut être utilié par l'utilisateur  ##
        if ref_qcm_allow(request.args.get('ref')) == False:
            return redirect(url_for('home', id="list_qcm"))

        qcm = request.args['ref'] + ".xml"

        ## Correction
        note = 0
        path_qcm = PATH_QCM_CORRECTION + qcm
        tree = etree.parse(path_qcm)

        for number in tree.xpath("/QCMCorrection/correction/question/@num"):
            radio_value = "question_" + number + "_awswer"
            #print(radio_value)
            xurl = "/QCMCorrection/correction/question[@num=" + number + "]/@id"
            if request.form.get(radio_value) == tree.xpath(xurl)[0]:
                note += 1

        html = "Tu as " + str(note) + " sur " + str(number)
        return html

    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
