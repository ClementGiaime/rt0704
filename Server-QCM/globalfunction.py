# -*- coding:utf-8 -*-
from flask import Flask, session, redirect, url_for, escape, request, render_template
import re
from lxml import etree
from os import listdir, remove, path
from conf import *


#####=======================================================================================####
###   Return True si les varaibles de session username, formation, listmatiere sont définie  ###
def session_is_define():
    if 'username' in session and 'formation' in session and 'listmatiere' in session :
        return True
    else :
        return False


#####===================================================================####
###   Test si la chaine ne contient que des caractères de la whitelist   ###
def string_match(string, regexp = r'[A-Za-z0-9]+'):
    return bool(re.fullmatch(regexp, string))


#####================================================================================================####
###   Test pour tout les éléments de la liste, si il ne contient que des caractères de la whitelist   ###
def list_string_match(list, regexp = r'[A-Za-z0-9]+'):
    ## Si la liste est vide return False
    if not list:
        return False

    for string in list:
        if string_match(string, regexp) == False:
            return False

    return True


#####===============================================================================#####
###   Test si l'utilisateur donné existe dans la base de permission xml               ###
###   Retourne une liste ["nom","formation","grade",["matiere1","matiere2"...,"matieren"] ]   ###
def request_session(username):
    tree = etree.parse("xml/perm.xml")

    xurl = "/utilisateurs/util[nom='" + username + "']/nom"
    user_request = tree.xpath(xurl)
    if not tree.xpath(xurl) :
        return False

    xurl = "/utilisateurs/util[nom='" + username + "']/formation"
    formation_request = tree.xpath(xurl)

    xurl = "/utilisateurs/util[nom='" + username + "']/grade"
    grade_request = tree.xpath(xurl)

    xurl = "/utilisateurs/util[nom='" + username + "']/listmatiere/matiere"
    listmatiere_request = tree.xpath(xurl)

    listmatiere_string = []
    for matiere in listmatiere_request:
        listmatiere_string.append(matiere.text)

    return [user_request[0].text, formation_request[0].text, grade_request[0].text, listmatiere_string]


def request_session_xml(xml):
    tree = etree.fromstring(xml)

    xurl = "/util/result"
    result_request = tree.xpath(xurl)[0].text

    if result_request == 'False' :
        #print(tree.xpath("/util/info")[0].text)
        return False

    xurl = "/util/nom"
    user_request = tree.xpath(xurl)[0].text

    xurl = "/util/formation"
    formation_request = tree.xpath(xurl)[0].text

    xurl = "/util/grade"
    grade_request = tree.xpath(xurl)[0].text

    xurl = "/util/listmatiere/matiere"
    listmatiere_request = tree.xpath(xurl)

    listmatiere_string = []
    for matiere in listmatiere_request:
        listmatiere_string.append(matiere.text)

    return [user_request, formation_request, grade_request, listmatiere_string]






#####==================================================================================================#####
###   Retourne une liste des fichiers du le dossier path et dont le nom des fichers correspondent à la regexp   ###
###   list = ["qcm-1","qcm-2","qcm-3","qcm-n"]
def list_dir(path, regexp):
    list = []
    #print(listdir(path))
    for file in listdir(path):
        if string_match(file, regexp) == True :
            list.append(file)
    return list

#####=============================================================================================================#####
###   Retourne une liste des fichiers avec des informations type de formation, type de matiere et nom de l'auteur   ###
###   list = [ [ xml, formation, matiere, auteur], [ xml-2, formation, matiere, auteur]  ]
def list_xml_info(path, list_xml, formation, listmatiere) :
    list_qcm_info = []

    for xml in list_xml :
        xurl = path + xml
        tree = etree.parse(xurl)
        info = [ xml, tree.xpath("/QCM/formation")[0].text, tree.xpath("/QCM/matiere")[0].text, tree.xpath("/QCM/auteur")[0].text ]
        list_qcm_info.append(info)

    return list_qcm_info

#####=================================================#####
###   Retourne True si l'étudiant peut utilisé le qcm   ###
###   Retourne False si il n'a pas le droit             ###
def xml_allow_etudiant(path, xml, formation, listmatiere) :
    xurl = path + xml
    tree = etree.parse(xurl)
    if formation in tree.xpath("/QCM/formation")[0].text and tree.xpath("/QCM/matiere")[0].text in listmatiere :
        return True
    else :
        return False

#####=================================================#####
###   Retourne True si le prof peut utilisé le qcm   ###
###   Retourne False si il n'a pas le droit             ###
def xml_allow_professeur(path, xml, auteur, listmatiere) :
    xurl = path + xml
    tree = etree.parse(xurl)
    if tree.xpath("/QCM/auteur")[0].text in auteur and tree.xpath("/QCM/matiere")[0].text in listmatiere :
        return True
    else :
        return False

#####=========================================================================================================================#####
###   Retourne une liste des fichiers dont l'utilisateur peut utiliser, critère en fonction de la formation et de la matiere   ###
def list_xml_allow(path, list_xml, formation, listmatiere, grade, nom) :

    list_qcm_allow = []
    for xml in list_xml:
        if grade == "etudiant" :
            if xml_allow_etudiant(path, xml, formation, listmatiere) == True :
                list_qcm_allow.append(xml)
        elif grade == "professeur" :
            if xml_allow_professeur(path, xml, nom, listmatiere) :
                list_qcm_allow.append(xml)

    return list_qcm_allow



####=========================================================================================####
##  Vérification de chaque champ du formulaire                                                 ##
##  Si un champ n'a pas la bonne syntaxe, initialisation d'un variable de session ERROR        ##
##  Et redirection vers le formulaire de création de qcm                                       ##
##  +                                                                                          ##
##  Vérifie si la ou les formation et la matiere sont inclu dans les permissions du professeur ##
def form_allow(name, formation, matiere, question, answer):
## name = "string", formation = ["ASR","CHPS"], matiere = ["RT0701"], question = "number", answer = "number"
    if string_match(name, REGEXP_NAME_QCM) == False:
        session['error_create_qcm'] = "* Le nom n'est pas conforme"
        return False

    ## Compte le nombre de formation
    number_formation_form = len(formation)
    ## Compare la liste des formation autorisée et la liste des formation envoyée par le formulaire
    number_formation_set = len(set(formation) & set(session['formation'].split(",")))
    ## Si number_formation_set == number_formation_form, cela veut dire que la liste des formation envoyée
    ## par le formulaire est autorisée pour le professeur

    if list_string_match(formation, REGEXP_NAME_FORMATION) == False or not number_formation_form == number_formation_set:
        session['error_create_qcm'] = "* Erreur sur la ou les Formation"
        return False

    if list_string_match(matiere, REGEXP_NAME_MATIERE) == False or not matiere[0] in session['listmatiere']:
        session['error_create_qcm'] = "* Erreur sur la matière"
        return False

    if string_match(question, REGEXP_NUMBER_QUESTION) == False:
        session['error_create_qcm'] = "* Le nombre de question de 1 à 99"
        return False

    if string_match(answer, REGEXP_NUMBER_ANSWER) == False:
        session['error_create_qcm'] = "* Le nombre de réponse de 1 à 9 par question"
        return False

    return True





def qcm_list_question_anwser(path, qcm):
    ## List = [ [ ["number","Question 1"],[ ["number","Réponse 1" ], ["number","Réponse 2" ] ] ],
    ##        [ [ ["number","Question 2"],[ ["number","Réponse 1" ], ["number","Réponse 2" ] ] ] ]
    list_question_anwser = []
    path_qcm = path + qcm

    tree = etree.parse(path_qcm)
    number_of_question = int(tree.xpath("count(/QCM/contenu/question)"))
    #print("Number of question : " + str(number_of_question))

    for number in range(1, number_of_question+1):
        list_temp = []
        ## Nom de la Question
        xurl = "/QCM/contenu/question[@num=" + str(number) + "]/intitule"
        intitule = [ number, tree.xpath(xurl)[0].text ]

        xurl = "count(/QCM/contenu/question[@num=" + str(number) + "]/reponses/reponse)"
        number_of_anwser = int(tree.xpath(xurl))
        #print("Number of anwser : " + str(number_of_anwser))


        for cpt in range(1, number_of_anwser+1):
            ## Nom de la réponse
            xurl = "/QCM/contenu/question[@num=" + str(number) + "]/reponses/reponse[@id=" + str(cpt) + "]"
            reponse = [ cpt, tree.xpath(xurl)[0].text ]
            list_temp.append(reponse)

        question_anwser = [ intitule, list_temp ]
        list_question_anwser.append(question_anwser)

    #print(list_question_anwser)
    return list_question_anwser




def remove_file(path, qcm):
    path_file = path + qcm
    remove(path_file)
    return True



####=======================================================================####
##  Vérification du nom du qcm                                               ##
##  Retourne True si il existe un déjà un QCM avec le même nom donné dans le formulaire    ##
def qcm_name_exist(path, name_qcm):
    list_xml = list_dir(path, r'.*(.xml)$')
    name_qcm = name_qcm + ".xml"
    for xml in list_xml:
        if name_qcm == xml:
            return True
    return False



####=====================================================================####
##  Vérifie si l'argument ?ref= existe                                     ##
##  Si il existe, test si la référence contient des caractères incorrecte  ##
##  Vérifie si le QCM peut être utilié par l'utilisateur                   ##
##  /delete_qcm /faire_qcm /correction_qcm                                 ##
def ref_qcm_allow(name_qcm):
    if name_qcm is None:
        session['error_list_qcm'] = "ERREUR - La référence du QCM n'existe pas"
        return False

    if string_match(name_qcm, REGEXP_NAME_QCM) == False :
        session['error_list_qcm'] = "ERROR - La référence possède un ou des caractères incorrecte"
        return False

    ####====================================================####
    ##  Vérifie si le QCM peut être utilié par l'utilisateur  ##
    list_xml = list_dir(PATH_QCM, r'.*(.xml)$')
    qcm_allow = list_xml_allow(PATH_QCM, list_xml, session['formation'], session['listmatiere'], session['grade'], session['username'])

    qcm = name_qcm + ".xml"

    if not qcm in qcm_allow:
        session['error_list_qcm'] = "ERROR - Le QCM n'existe pas ou tu n'as pas les droits nécéssaire pour le faire"
        return False

    return True
