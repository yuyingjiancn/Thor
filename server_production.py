# -*- coding: utf-8 -*-
from bottle import run, TEMPLATE_PATH
from routes import static, admin, student

TEMPLATE_PATH[:] = ['templates']

run(host='0.0.0.0', port=80, server="tornado")