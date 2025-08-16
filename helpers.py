
from flask import request

from flask import redirect, render_template, session
from functools import wraps


def apology(message, code=400):
    """Render message as an HTML file"""
    return render_template("apology.html", top=code, bottom=message), code

def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function

