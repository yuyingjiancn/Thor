# -*- coding: utf-8 -*-
import sqlite3
import json
from bottle import get, post, request, response, redirect, jinja2_view


@get('/student/login')
@jinja2_view('student/login.html')
def student_login_get():
    return {}


@post('/student/login')
@jinja2_view('student/login.html')
def student_login_post():
    no = request.forms.get('no')
    name = request.forms.get('name')
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    c.execute('SELECT id FROM students WHERE no = ? AND name = ?',
              (no, name))
    student = c.fetchone()
    conn.close()

    if student is None:
        return {'errors': '学号和姓名对不上'}
    else:
        response.set_cookie('id', str(student[0]))
        redirect('/student/index')

@get('/student/index')
@jinja2_view('student/index.html')
def student_index_get():
    if not request.get_cookie('id'):
        redirect('/student/login')
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    c.execute('SELECT id, name FROM exercises')
    exercises = c.fetchall()
    conn.close()
    return {'exercises': exercises}

@get('/student/exercise/<eid>')
@jinja2_view('student/exercise.html')
def student_exercise_get(eid):
    if not request.get_cookie('id'):
        redirect('/student/login')
    student_id = int(request.get_cookie('id'))

    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    c.execute('SELECT id, no, name, class_id FROM students WHERE id = ?', (student_id, ))
    student = c.fetchone()
    conn.close()
    if student is None:
        redirect('/student/login')

    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    c.execute('SELECT id, name, questions FROM exercises WHERE id = ?', (eid, ))
    exercise = list(c.fetchone())
    exercise[2] = json.loads(exercise[2])
    conn.close()
    if exercise is None:
        redirect('/student/index')

    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    c.execute('SELECT answer FROM answers WHERE student_id = ? AND exercise_id = ?', (student_id, eid,))
    answer = c.fetchone()
    if answer is None:
        answer = 'null'
    else:
        answer = answer[0]
    conn.close()
    return {'student': student, 'exercise': exercise, 'answer': answer}

@post('/student/exercise/post/<sid>/<eid>')
def student_exercise_post(sid, eid):
    if not request.get_cookie('id'):
        return {'success': False, 'message': '请登录'}
    student_id = int(request.get_cookie('id'))
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    c.execute('SELECT id, no, name, class_id FROM students WHERE id = ?', (student_id, ))
    student = c.fetchone()
    conn.close()
    if student is None:
        return {'success': False, 'message': '请登录'}
    data = request.POST.get('data')

    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    c.execute('SELECT * FROM answers WHERE student_id = ? AND exercise_id = ?', (sid, eid))
    answer = c.fetchone()
    conn.close()
    if answer is None:
        conn = sqlite3.connect('db.sqlite3')
        c = conn.cursor()
        c.execute('INSERT INTO answers (student_id, exercise_id, answer) VALUES (?, ?, ?)', (sid, eid, data))
        conn.commit()
        conn.close()
    else:
        conn = sqlite3.connect('db.sqlite3')
        c = conn.cursor()
        c.execute('UPDATE answers SET answer = ? WHERE student_id = ? AND exercise_id = ?', (data, sid, eid))
        conn.commit()
        conn.close()
    return {'success': True}