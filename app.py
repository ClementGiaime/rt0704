# -*- coding:utf-8 -*-
from flask import Flask, session, redirect, url_for, escape, request

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello !"

@app.route('/login')
def login():
    return "Page de login"

@app.route('/home')
def home():
    return "Page home après authentification"

@app.route('/config_QCM')
def config_qcm():
    return "Page de configuration avant la création du QCM (Nom du QCM, Matiere, Nombre de question)"

@app.route('/create_QCM')
def create_qcm():
    return "Page de création du QCM, ne s'affiche que quand l'on a configurer le QCM"

@app.route('/list_qcm')
def list_qcm():
    return "Page de choix des QCM"

if __name__ == '__main__':
    app.run(debug=True)
