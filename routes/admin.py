# -*- coding: utf-8 -*-
import sqlite3
import json
import math
from bottle import get, post, request, response, redirect, jinja2_view


@get("/admin/login")
@jinja2_view("admin/login.html")
def admin_login_get():
    return {}


@post("/admin/login")
@jinja2_view("admin/login.html")
def admin_login_post():
    account = request.forms.get("account")
    password = request.forms.get("password")
    conn = sqlite3.connect("db.sqlite3")
    c = conn.cursor()
    c.execute(
        "SELECT id FROM admins WHERE account = ? AND password = ?", (account, password)
    )
    admin = c.fetchone()
    conn.close()

    if admin is None:
        return {"errors": "账号或密码错误"}
    else:
        response.set_cookie("admin_id", str(admin[0]))
        redirect("/admin/index")


@get("/admin/index")
@jinja2_view("admin/index.html")
def admin_index_get():
    if not request.get_cookie("admin_id"):
        redirect("/admin/login")

    conn = sqlite3.connect("db.sqlite3")
    c = conn.cursor()
    c.execute("SELECT id, name FROM classes")
    classes = c.fetchall()
    conn.close()

    conn = sqlite3.connect("db.sqlite3")
    c = conn.cursor()
    c.execute("SELECT id, name FROM exercises")
    exercises = c.fetchall()
    conn.close()
    return {"classes": classes, "exercises": exercises}


@get("/admin/exercise/create")
@jinja2_view("admin/exercise_create.html")
def admin_exercise_create_get():
    if not request.get_cookie("admin_id"):
        redirect("/admin/login")
    return {}


@post("/admin/exercise/create")
@jinja2_view("admin/exercise_create.html")
def admin_exercise_create_post():
    if not request.get_cookie("admin_id"):
        redirect("/admin/login")
    name = request.forms.get("name")
    questions = request.forms.get("questions")

    conn = sqlite3.connect("db.sqlite3")
    c = conn.cursor()
    c.execute("INSERT INTO exercises (name, questions) VALUES(?, ?)", (name, questions))
    conn.commit()
    conn.close()
    redirect("/admin/index")


@get("/admin/exercise/view/<eid>/<cid>")
@jinja2_view("admin/exercise_view.html")
def admin_exercise_view_get(eid, cid):
    if not request.get_cookie("admin_id"):
        redirect("/admin/login")

    conn = sqlite3.connect("db.sqlite3")
    c = conn.cursor()
    c.execute("SELECT id, name, questions FROM exercises WHERE id = ?", (eid,))
    exercise = list(c.fetchone())
    questions = json.loads(exercise[2])
    conn.close()

    da = {}
    for q in questions:
        da[q[0]] = 0

    conn = sqlite3.connect("db.sqlite3")
    c = conn.cursor()
    c.execute(
        "SELECT answer FROM answers WHERE exercise_id = ? AND student_id IN (SELECT id FROM students WHERE class_id = ?)",
        (eid, cid),
    )
    answers = c.fetchall()
    conn.close()
    answers = [json.loads(a[0]) for a in answers]
    answers_count = len(answers)

    for a in answers:
        for q in questions:
            if a.get(q[0], "False") == "True":
                da[q[0]] += 1

    da1 = {}
    for k, v in da.items():
        da1[k] = round(v / answers_count * 100, 2)

    conn = sqlite3.connect("db.sqlite3")
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM students WHERE class_id = ?", (cid,))
    student_count = c.fetchone()[0]
    conn.close()

    da2 = {}
    for k, v in da.items():
        da2[k] = round(v / student_count * 100, 2)

    return {"exercise": exercise, "da1": da1, "da2": da2}

