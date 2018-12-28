# -*- coding:utf-8 -*-
from flask import Flask, session, redirect, url_for, escape, request, render_template
import re

def sessionIsDefine():
    if 'username' in session and 'formation' in session and 'listmatiere' in session :
        return True
    else :
        return False


def string_match(string, regexp = r'[^A-Za-z0-9]'):
    return not bool(re.compile(regexp).search(string))
