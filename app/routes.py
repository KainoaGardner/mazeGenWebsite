from flask import render_template, session, request, redirect, flash, url_for
from app import app
from app.mazeClass import getImage, makeMaze


@app.route("/", methods=["GET", "POST"])
@app.route("/home", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        if "generate" in request.form:
            maze = makeMaze()
            getImage(maze)
            image = "maze"
            session["maze"] = maze.__dict__
        elif "solve" in request.form:
            image = "solve"
        elif "download" in request.form:
            if "maze" in session:
                pass

        maze = session["maze"]

        return render_template("home.html", maze=maze, image=image)

    else:
        if "maze" in session:
            maze = session["maze"]
            return render_template("home.html", maze=maze)
        else:
            return render_template("home.html", maze=None)
