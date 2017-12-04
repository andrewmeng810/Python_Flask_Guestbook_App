#!/usr/bin/env python

import flask
from flask import Flask, render_template, request, redirect, url_for
import datetime
import sqlite3

from sqlite3 import Error

DATABASE = r"/guestbook_db.db"     # Create the database global variable
conn = sqlite3.connect(DATABASE)    # initiate database connection
c = conn.cursor()                   # create cursor

app = flask.Flask(__name__)           # a Flask object


@app.route('/home')
def homepage():
    """ This is the homepage for the gustbook app """
    return flask.render_template('home.html', posts = showpost())
    # refer posts in showpost function to query all entries for guestbook_id = 1


@app.route('/create/', methods=['POST', 'GET'])
def creat_post():
    """ to take form input and insert in to local database """
    name = request.form["name"]     # from a POST (form with 'method="POST"')
    comment = request.form["comment"]     # from a POST (form with 'method="POST"')
    insert_records(name, comment)

    return flask.render_template('home.html')

def insert_records(name, comment):
    """ Insert into local sqlite database """
    conn = sqlite3.connect(DATABASE)    # initiate database connection
    c = conn.cursor()                   # create cursor
    comment_time = datetime.datetime.now().strftime("%B %d, %Y %I:%M%p")

    c.execute(
    """
    INSERT INTO entry VALUES (1,{},{},{})
    """.format(name, comment, comment_time)
    )
    conn.commit()


def showpost():
    """ Show all entries """
    conn = sqlite3.connect(DATABASE)    # initiate database connection
    c = conn.cursor()                   # create cursor

    entries = c.execute(
    """
    SELECT * FROM entry
    WHERE entry.guestbook_id = 1
    """).fetchall()
    conn.commit()
    conn.close()
    return entries



if __name__ == '__main__':
    app.run(debug=True, port=8000)    # app starts serving in debug mode on port 5000
