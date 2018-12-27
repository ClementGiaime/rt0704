# -*- coding:utf-8 -*-
from flask import Flask, session, redirect, url_for, escape, request, render_template

def sessionIsDefine():
    if 'username' in session and 'formation' in session and 'listmatiere' in session :
        return True
    else :
        return False
