# -*- coding: utf-8 -*-
import os
from bottle import route, static_file

@route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(
        filepath,
        root=f"{os.path.dirname(os.path.abspath(__file__))}\\..\\static\\")