# -*- coding: utf-8 -*-
import sqlite3
from bottle import get, post, request, response, redirect, jinja2_view


@get('/admin/login')
@jinja2_view('admin/login.html')
def admin_login_get():
    return {}


@post('/admin/login')
@jinja2_view('admin/login.html')
def admin_login_post():
    account = request.forms.get('account')
    password = request.forms.get('password')
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    c.execute('SELECT id FROM admins WHERE account = ? AND password = ?',
              (account, password))
    admin = c.fetchone()
    conn.close()

    if admin is None:
        return {'errors': '账号或密码错误'}
    else:
        response.set_cookie('admin_id', str(admin[0]))
        redirect('/admin/index')

@get('/admin/index')
@jinja2_view('admin/index.html')
def admin_index_get():
    if not request.get_cookie('admin_id'):
        redirect('/admin/login')
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    c.execute('SELECT id, name FROM exercises')
    exercises = c.fetchall()
    conn.close()
    return {'exercises': exercises}

@get('/admin/exercise/create')
@jinja2_view('admin/exercise_create.html')
def admin_exercise_create_get():
    if not request.get_cookie('admin_id'):
        redirect('/admin/login')
    return {}

@post('/admin/exercise/create')
@jinja2_view('admin/exercise_create.html')
def admin_exercise_create_post():
    if not request.get_cookie('admin_id'):
        redirect('/admin/login')
    name = request.forms.get('name')
    questions = request.forms.get('questions')

    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    c.execute(
        'INSERT INTO exercises (name, questions) VALUES(?, ?)',
        (name, questions))
    conn.commit()
    conn.close()
    redirect('/admin/index')
