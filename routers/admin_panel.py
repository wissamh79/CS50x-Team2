from flask import Blueprint, session, request, render_template, flash, redirect
from database import db
import requests

admin_router = Blueprint(
    "admin_router",
    __name__,
    static_folder="../static/",
    template_folder="../templates",
)


@admin_router.route("/")
def admin_specialty_list():
    specialty = db.execute("SELECT * FROM specialty;")
    return render_template("admin/adminLayout.html", specialty=specialty)


@admin_router.route("/specialty_add", methods=["GET", "POST"])
def admin_specialty_add():
    if request.method == "GET":
        specialty = db.execute("SELECT id, name, FROM specialty ORDER BY name ASC;")
        
        return render_template(
            "admin/specialty_add.html", data={"specialty": specialty}
        )
    else:
        name = request.form.get("name")
        image = request.files.get("image")

        res = requests.post(
            "https://api.imgbb.com/1/upload",
            files={"image": image},
            params={"key": "b541fcbfce81e58bba252fdd01197bbf"},
        )
        if res.ok:
            data = res.json()
            image = data["data"]["url"]
        else:
            image = ""
        # Insert specialties table information
        specialty = db.execute(
            """
                   INSERT INTO specialty 
                   (name, image)
                   """,
            name,
            image,
        )
        return redirect("/admin")
    
@admin_router.route("/specialty")
def admin_doctor_list():
    Doctor = db.execute("SELECT * FROM Doctor;")
    return render_template("admin/specialty/specialty_add.html", Doctor=Doctor)


@admin_router.route("/specialty/doctor_add", methods=["GET", "POST"])
def admin_doctors_add():
    if request.method == "GET":
        Doctor = db.execute("SELECT id, name, specialty, description, doctors_address FROM Doctor ORDER BY name ASC;")
        
        return render_template(
            "admin/specialty/Doctor_add.html", data={"name": name, "specialty": specialty }
        )
    else:
        name = request.form.get("name")
        description = request.form.get("description")
        phone = request.form.get("phone")
        email = request.form.get("email")
        gender = request.form.get("gender")
        specialty = request.form.get("specialty")
        is_available = True if request.form.get("is_available") == "on" else False
        years_of_practice = request.form.getlist("years_of_practice")
        doctors_address = request.form.getlist("doctors_address")
        user_id = request.form.getlist("user_id")

        res = requests.post(
            "https://api.imgbb.com/1/upload",
            files={"image": image},
            params={"key": "b541fcbfce81e58bba252fdd01197bbf"},
        )
        if res.ok:
            data = res.json()
            image = data["data"]["url"]
        else:
            image = ""
        # Insert Doctors table information
        Doctor = db.execute(
            """
                   INSERT INTO Doctor 
                   (name, description, specialty, phone, 
                   email, gende, is_available, years_of_practice, doctors_address, user_id)
                   """,
            name,
            description,
            specialty,
            phone,
            email,
            gender,
            bool(is_available),
            years_of_practice,
            doctors_address,
            user_id,
        )
        return redirect("/admin/specialty/doctor_add")
    

@admin_router.route("/specialty/edit", methods=["GET", "POST"])
def admin_specialty_edit():
    if request.method == "GET":
        try:
            specialty = db.execute("SELECT * FROM specialty ORDER BY name ASC;")[0]
        except:
            return render_template("404.html")
        genres = db.execute(
            """SELECT genres.id AS id,genres.name AS name, 
            CASE WHEN movies_genres.movie_id IS NULL THEN 0 ELSE 1 END AS exist
            FROM genres LEFT JOIN movies_genres ON genres.id = movies_genres.genre_id
            AND movies_genres.movie_id = ?""",
            movie_id,
        )

        actors = db.execute(
            """SELECT people.id as id, people.name as name,
            CASE WHEN movies_actors.movie_id IS NULL THEN 0 ELSE 1 END AS exist
            FROM people LEFT JOIN movies_actors ON people.id = movies_actors.people_id
            AND movies_actors.movie_id = ?;""",
            movie_id,
        )

        directors = db.execute(
            """SELECT people.id as id, people.name as name,
            CASE WHEN movies_directors.movie_id IS NULL THEN 0 ELSE 1 END AS exist
            FROM people LEFT JOIN movies_directors ON people.id = movies_directors.people_id
            AND movies_directors.movie_id = ?;""",
            movie_id,
        )

        return render_template(
            "admin/movies/movie_edit.html",
            movie=movie,
            genres=genres,
            directors=directors,
            actors=actors,
        )

    # Post Method
    else:
        genres = request.form.getlist("genres")
        actors = request.form.getlist("actors")
        directors = request.form.getlist("directors")
        title = request.form.get("title")
        release = request.form.get("release")
        description = request.form.get("description")
        length = request.form.get("length")
        rating = request.form.get("rating")
        trailer = request.form.get("trailer")
        is_featured = True if request.form.get("is_featured") == "on" else False
        image = request.files.get("poster", None)

        # If changed image, Upload new image.
        if image:
            res = requests.post(
                "https://api.imgbb.com/1/upload",
                files={"image": image},
                params={"key": "b541fcbfce81e58bba252fdd01197bbf"},
            )
            if res.ok:
                data = res.json()
                image = data["data"]["url"]
        else:
            image = db.execute("SELECT poster FROM movies WHERE id=?", movie_id)[0][
                "poster"
            ]
        # Start updating
        db.execute(
            """
                   UPDATE movies SET title = ?, description = ?, release = ? , length = ?, rating = ?, poster = ?, trailer = ?, is_featured = ? WHERE id = ?;
                   """,
            title,
            description,
            release,
            length,
            float(rating),
            image,
            trailer,
            bool(is_featured),
            movie_id,
        )
        db.execute(
            """
                   INSERT INTO movies_genres (movie_id, genre_id)
                   
                    SELECT ? AS movieID, genres.id AS GenreID
                    FROM genres WHERE genres.id IN (?)
                    AND genres.id NOT IN (
                    SELECT genre_id FROM movies_genres WHERE movie_id = ?);
                   """,
            movie_id,
            genres,
            movie_id,
        )

        db.execute(
            """
                   INSERT INTO movies_actors (movie_id, people_id)
                   
                    SELECT ? AS movieID, people.id AS peopleID
                    FROM people WHERE people.id IN (?)
                    AND people.id NOT IN (
                    SELECT people_id FROM movies_actors WHERE movie_id = ?);
                   """,
            movie_id,
            actors,
            movie_id,
        )
        db.execute(
            """
                   INSERT INTO movies_directors (movie_id, people_id)
                   
                    SELECT ? AS movieID, people.id AS peopleID
                    FROM people WHERE people.id IN (?)
                    AND people.id NOT IN (
                    SELECT people_id FROM movies_directors WHERE movie_id = ?);
                   """,
            movie_id,
            directors,
            movie_id,
        )
        return redirect("/admin/movies")


@admin_router.route("/people")
def admin_people_list():
    people = db.execute("SELECT * FROM people;")
    return render_template("admin/people/people_list.html", people=people)


@admin_router.route("/people/add", methods=["GET", "POST"])
def admin_people():
    if request.method == "GET":
        return render_template("admin/people/people_add.html")

    name = request.form.get("name", None)
    image = request.files.get("photo")
    print(request.files)

    if image:
        res = requests.post(
            "https://api.imgbb.com/1/upload",
            files={"image": image},
            params={"key": "b541fcbfce81e58bba252fdd01197bbf"},
        )
        if res.ok:
            data = res.json()
            image = data["data"]["url"]
            print(image)

    try:
        db.execute("INSERT INTO people (name, photo) VALUES (?,?);", name, image)
    except Exception as e:
        print(f"An Error has been generated\n".upper() + e)
        return render_template("failure.html")
    return redirect("/admin/people")


@admin_router.route("/people/<people_id>/edit", methods=["GET", "POST"])
def admin_people_edit(people_id):
    try:
        person = db.execute("SELECT * FROM people WHERE id = ?;", people_id)[0]
    except:
        return render_template("failure.html")
    if request.method == "GET":
        return render_template("admin/people/people_edit.html", person=person)

    name = request.form.get("name")
    image = request.files.get("photo")

    if not image:
        try:
            image = db.execute("SELECT photo FROM people WHERE id = ?")[0]["photo"]
        except:
            return render_template("failure.html")
    else:
        res = requests.post(
            "https://api.imgbb.com/1/upload",
            files={"image": image},
            params={"key": "b541fcbfce81e58bba252fdd01197bbf"},
        )
        if res.ok:
            data = res.json()
            image = data["data"]["url"]
    db.execute("UPDATE people SET name = ?, photo = ?", name, image)
    return redirect("/admin/people")
