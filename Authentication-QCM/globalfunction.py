# -*- coding:utf-8 -*-
#from flask import Flask, session, redirect, url_for, escape, request, render_template
#import re
from lxml import etree
from conf import *



def request_session(username):
    """
    Test si l'utilisateur donné existe dans la base de permission xml
    Retourne : liste ["nom","formation","grade",["matiere1","matiere2"...,"matieren"] ]
    """
    tree = etree.parse(PATH_PERMISSION)

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
