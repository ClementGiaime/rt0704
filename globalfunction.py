# -*- coding:utf-8 -*-
from flask import Flask, session, redirect, url_for, escape, request, render_template
import re
from lxml import etree
from os import listdir

#####========================================####
###   Test si le client possède une session   ###
def sessionIsDefine():
    if 'username' in session and 'formation' in session and 'listmatiere' in session :
        return True
    else :
        return False

#####===================================================================####
###   Test si la chaine ne contient que des caractères de la whitelist   ###
def string_match(string, regexp = r'[A-Za-z0-9]'):
    return bool(re.compile(regexp).search(string))


def request_session(username):
    tree = etree.parse("xml/perm.xml")

    xurl = "/utilisateurs/util[nom='" + username + "']/nom"
    user_request = tree.xpath(xurl)
    if not tree.xpath(xurl) :
        return False

    xurl = "/utilisateurs/util[nom='" + username + "']/formation"
    formation_request = tree.xpath(xurl)

    xurl = "/utilisateurs/util[nom='" + username + "']/listmatiere/matiere"
    listmatiere_request = tree.xpath(xurl)

    listmatiere_string = []
    for matiere in listmatiere_request:
        listmatiere_string.append(matiere.text)

    return [user_request[0].text, formation_request[0].text, listmatiere_string]

def list_dir(path, regexp):
    list = []
    print(listdir(path))
    for file in listdir(path):
        if string_match(file, regexp) == True :
            list.append(file)
    return list

def list_xml_allow(path, list_xml, formation, listmatiere) :

    list_qcm_allow = []
    for xml in list_xml:
        xurl = path + xml
        tree = etree.parse(xurl)
        print(tree.xpath("/QCM/formation")[0].text)
        print(tree.xpath("/QCM/matiere")[0].text)
        if tree.xpath("/QCM/formation")[0].text == formation and tree.xpath("/QCM/matiere")[0].text in listmatiere :
            list_qcm_allow.append(xml)


    return list_qcm_allow
