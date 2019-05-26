# -*- coding: utf-8 -*-
from bottle import run, TEMPLATE_PATH
from routes import static, admin

TEMPLATE_PATH[:] = ['templates']



run(host='localhost', port=80, reloader=True, debug=True)