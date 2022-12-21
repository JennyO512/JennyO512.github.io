import os
import datetime
from tkinter import INSERT
import requests
import urllib.parse

from flask import Flask
from flask import flash, redirect, render_template, session, request, jsonify, make_response, url_for
from flask_session import Session
from tempfile import mkdtemp
from cs50 import SQL
from cs50 import get_int, get_string
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps
import threading

app = Flask(__name__)

NOTES = {}

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Database
db = SQL("sqlite:///stuff2do.db")


def login_required(f):
    """
    Decorate routes to require login.
    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


# Home page of the website
@app.route("/")
@login_required
def index():
    return render_template("index.html")


# Registration page
@app.route("/register", methods=["GET", "POST"])
def register():

    """Register user"""
    if request.method == "GET":
        return render_template("register.html")

    else:
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:
            return render_template("No Username Given")
        if not password:
            return render_template("No Passowrd Given")
        if not confirmation:
            return render_template("Passwords do not Match")

        if password != confirmation:
            return render_template("Password and confirmation do not match")

        hash = generate_password_hash(password)

        try:
            new_user = db.execute("INSERT INTO user (username, hash) VALUES (?, ?)", username, hash)

        except:
             return render_template("Username already is there, pendeja")

        session["user_id"] = new_user

        return redirect("/")

# Login page
@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Error checking if the user does not enter information properly
        if not username:
            return render_template("apology.html", message="Make sure to enter a username"), 403
        elif not password:
            return render_template("apology.html", message="Make sure to enter a password"), 403

        # Query database for username
        rows = db.execute("SELECT * FROM user WHERE username = ?", request.form.get("username"))

       # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return render_template("apology.html", message="invalid username and/or password"), 403

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


# Notes page
@app.route("/notes")
@login_required
def notes():
    """
    Shows the notes for the user
    """

    user_id = session["user_id"]

    Note = db.execute("SELECT * FROM note WHERE user_id = ?", user_id)

    return render_template("stuff.html", notes = Note)


@app.route("/notes/add-note", methods=["GET", "POST"])
@login_required
def add_note():
    """
    Adds a new note
    """
    if request.method == "GET":
        return render_template("add.html")
    else:
        # Get the note
        new_note = request.form.get("new_note")

        user_id = session["user_id"]


        # Add note to database
        db.execute("INSERT INTO note (notes, user_id) VALUES (?,?)", new_note, user_id)

        flash("Added note!")
        return redirect("/notes")


@app.route("/notes/delete-note", methods=["POST"])
def delete_note():
    """
    Deletes a note
    """
    note_id = request.form.get("note-id")
    if 'note-id':
        db.execute("DELETE from note where id = ?", note_id)
    return redirect("/notes")


@app.route("/contact", methods=["GET", "POST"])
@login_required
def contact():
    """
    Writes the user message to a local file in the directory
    """
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")

        with open("messages.txt", "a") as messageFile:
            messageFile.write(f"Message by {name}\n")
            messageFile.write(f"User email: {email}\n")
            messageFile.write(f"User message: {message}\n")
            messageFile.write("\n")

        flash("Your message has been sent!")
        return redirect("/contact")

    else:
        return render_template("contact.html")



@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")



if __name__ == "__main__":
    app.run()