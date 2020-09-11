"""
A mock-up Flask implementation of an API endpoint for O'Reilly books and other media. Can load data
directly from the official API into Postgres. Supports adding data via POST (parameterized and as
json), or via an HTML form. Returns data as json, either by attribute or all at once.
"""

__author__ = "Brad Frank"

import json
import ssl
import urllib.request
from flask import Flask, jsonify, request, render_template, Markup
from flask_sqlalchemy import SQLAlchemy
from .config import config # Flask app config files.

app = Flask(__name__)
app.config.from_object(config.Config)
db = SQLAlchemy(app)

from .models.works import Works # Database and table scaffolding.

db.create_all()
db.session.commit()

@app.route("/load")
def load():
    """
    Loads data from the official O'Reilly API. Currently doesn't do error checking. Also transforms
    author list into a single string (semicolon for delimator) for simplicity.

    TODO: Break author data into a separate table with proper intersection table.
    """

    url = "https://learning.oreilly.com/api/v2/search/"
    fields = ["isbn", "authors", "title", "description"]
    limit = 200
    entry_counter = 0 # To confirm number of records loaded.

    api = "{}?query=python&limit={}&fields={}".format(url, limit, "&fields=".join(fields))

    ssl._create_default_https_context = ssl._create_unverified_context # Work around lack of https.
    response = urllib.request.urlopen(api)
    encoding = response.info().get_content_charset("utf-8")
    feed = json.loads(response.read().decode(encoding))

    for entry in feed["results"]:
        entry.setdefault("isbn", "")
        entry.setdefault("description", "")

        title = entry["title"]
        authors = "; ".join(entry["authors"])
        isbn = entry["isbn"]
        description = entry["description"]

        work = Works(
            title=title,
            authors=authors,
            isbn=isbn,
            description=description
        )

        db.session.add(work)
        db.session.commit()
        entry_counter += 1

    return render_template(
        "response.html",
        message="{} O'Reilly works successfully added.".format(entry_counter)
    )

@app.route("/index")
@app.route("/")
def main():
    """Provides a landing page with instructions and links."""
    return render_template("index.html")

@app.route("/add", methods=["GET", "POST"])
def add_work():
    """Adds data via parameterized and json POST calls."""

    if request.is_json:
        data = request.get_json()

        title = data["title"]
        authors = data["authors"]
        isbn = data["isbn"]
        description = data["description"]
    else:
        title = request.args.get("title")
        authors = request.args.get("authors")
        isbn = request.args.get("isbn")
        description = request.args.get("description")

    try:
        work = Works(
            title=title,
            authors=authors,
            isbn=isbn,
            description=description
        )
        db.session.add(work)
        db.session.commit()
        return "New work added as ID {}.".format(work.work_id)
    except Exception as err:
        return str(err)

@app.route("/add/form", methods=["GET", "POST"])
def add_work_form():
    """Adds data via an HTML form."""

    if request.method == "POST":
        title = request.form.get("title")
        authors = request.form.get("authors")
        isbn = request.form.get("isbn")
        description = request.form.get("description")

        try:
            work = Works(
                title=title,
                authors=authors,
                isbn=isbn,
                description=description
            )

            db.session.add(work)
            db.session.commit()

            message = Markup(
                "New work <a href=\"/get/{}\">({})</a> successfully added.".format(
                    work.work_id, work.work_id
                )
            )
            return render_template("response.html", message=message)
        except Exception as err:
            return str(err)

    return render_template("form.html")

@app.route("/get/all")
def get_all():
    """Returns all stored data as json."""

    try:
        works = Works.query.all()
        return jsonify([e.serialize() for e in works])
    except Exception as err:
        return str(err)

@app.route("/get/<id_>")
def get_by_id(id_):
    """Returns a single entry as json."""

    try:
        work = Works.query.filter_by(work_id=id_).first()
        return jsonify(work.serialize())
    except Exception:
        return "No entry for {}.".format(id_)

@app.route("/get")
def get_by_attribute():
    """Searches on work attributes, currently limited to a single attribute per search."""

    try:
        # Request to search by title:
        if "title" in request.args:
            title = "%{}%".format(request.args.get("title", type=str))
            works = Works.query.filter(Works.title.like(title)).all()

        # Request to search by author:
        elif "author" in request.args:
            authors = "%{}%".format(request.args.get("author", type=str))
            works = Works.query.filter(Works.authors.like(authors)).all()

        # Request to search by isbn:
        elif "isbn" in request.args:
            isbn = request.args.get("isbn", type=str)
            works = Works.query.filter_by(isbn=isbn).all()

        # Request to search by description:
        elif "description" in request.args:
            description = "%{}%".format(request.args.get("description", type=str))
            works = Works.query.filter(Works.description.like(description)).all()
        else:
            return "No query found."

        if len(works) == 0:
            return "No entries found."

        return jsonify([e.serialize() for e in works])
    except Exception as err:
        return str(err)

if __name__ == '__main__':
    app.run()
