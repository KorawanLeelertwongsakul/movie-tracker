from flask import Flask, render_template, request, redirect
import sqlite3
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# เชื่อม database
def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


# Home
@app.route("/")
def home():
    return render_template("home.html")


# แสดง movies
@app.route("/movies")
def movies():

    search = request.args.get("search")

    db = get_db()

    if search:
        movies = db.execute(
            "SELECT * FROM movies WHERE title LIKE ?",
            ('%' + search + '%',)
        ).fetchall()
    else:
        movies = db.execute(
            "SELECT * FROM movies"
        ).fetchall()

    db.close()
    return render_template("movies.html", movies=movies)


# ADD MOVIE 
@app.route("/add", methods=["GET", "POST"])
def add():

    if request.method == "POST":

        title = request.form["title"]
        genre = request.form["genre"]
        rating = request.form["rating"]
        review = request.form.get("review", "")

        image = request.files["image"]

        filename = ""

        if image and image.filename != "":
            filename = secure_filename(image.filename)
            image.save(
                os.path.join(
                    app.config['UPLOAD_FOLDER'],
                    filename
                )
            )

        db = get_db()

        db.execute(
            "INSERT INTO movies (title, genre, rating, image, review) VALUES (?, ?, ?, ?, ?)",
            (title, genre, rating, filename, review)
        )

        db.commit()
        db.close()

        return redirect("/movies")

    return render_template("add.html")


# DELETE MOVIE
@app.route("/delete/<int:id>")
def delete_movie(id):

    db = get_db()

    db.execute(
        "DELETE FROM movies WHERE id=?",
        (id,)
    )

    db.commit()
    db.close()

    return redirect("/movies")


# About
@app.route("/about")
def about():
    return render_template("about.html")


# Edit
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):

    db = get_db()

    if request.method == "POST":

        title = request.form["title"]
        genre = request.form["genre"]
        rating = request.form["rating"]
        review = request.form.get("review", "")

        db.execute(
            "UPDATE movies SET title=?, genre=?, rating=?, review=? WHERE id=?",
            (title, genre, rating, review, id)
        )

        db.commit()
        db.close()

        return redirect("/movies")

    movie = db.execute(
        "SELECT * FROM movies WHERE id=?",
        (id,)
    ).fetchone()

    db.close()

    return render_template("edit.html", movie=movie)


# Detail
@app.route("/movie/<int:id>")
def movie_detail(id):

    db = get_db()

    movie = db.execute(
        "SELECT * FROM movies WHERE id=?",
        (id,)
    ).fetchone()

    db.close()

    return render_template(
        "movie_detail.html",
        movie=movie
    )


@app.route("/contact")
def contact():
    return render_template("contact.html")


# Stats
@app.route("/stats")
def stats():

    db = get_db()

    total = db.execute(
        "SELECT COUNT(*) FROM movies"
    ).fetchone()[0]

    avg = db.execute(
        "SELECT AVG(CAST(rating AS FLOAT)) FROM movies"
    ).fetchone()[0]

    max_movie = db.execute(
        "SELECT * FROM movies ORDER BY CAST(rating AS FLOAT) DESC LIMIT 1"
    ).fetchone()

    db.close()

    return render_template(
        "stats.html",
        total=total,
        avg=avg,
        max_movie=max_movie
    )


@app.route("/top")
def top_movies():

    db = get_db()

    movies = db.execute(
        "SELECT * FROM movies ORDER BY CAST(rating AS FLOAT) DESC LIMIT 5"
    ).fetchall()

    db.close()

    return render_template(
        "top.html",
        movies=movies
    )


# Run
if __name__ == "__main__":
    app.run(debug=True)