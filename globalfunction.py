# -*- coding:utf-8 -*-
from flask import Flask, session, redirect, url_for, escape, request, render_template
import re
from lxml import etree

def sessionIsDefine():
    if 'username' in session and 'formation' in session and 'listmatiere' in session :
        return True
    else :
        return False

def string_match(string, regexp = r'[^A-Za-z0-9]'):
    return not bool(re.compile(regexp).search(string))

def usernameIsDefine(username):
    tree = etree.parse("xml-templates/perm.xml")
    for user in tree.xpath("/utilisateurs/util/nom") :
        print(user.text)
        if username == user.text :
            xurl = "/utilisateurs/util[nom='" + username + "']/formation"
            html = "<h1>Welcome !</h1>"
            for content in tree.xpath(xurl):
                html = html + content.text +"<br>"
            return html
