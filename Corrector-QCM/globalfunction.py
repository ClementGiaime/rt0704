# -*- coding:utf-8 -*-
#from flask import Flask, session, redirect, url_for, escape, request, render_template
#import re
from os import remove
from lxml import etree
#from conf import *

def remove_file(path, qcm):
    path_file = path + qcm
    remove(path_file)
    return True
