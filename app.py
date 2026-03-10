from flask import Flask, render_template, request, jsonify, redirect
import sqlite3
import sys
import io

import database

app = Flask(__name__)


# LOGIN PAGE

@app.route("/")
def login():
    return render_template("login.html")


# REGISTER PAGE

@app.route("/register")
def register():
    return render_template("register.html")


# CREATE USER

@app.route("/create_user",methods=["POST"])
def create_user():

    username=request.form["username"]
    password=request.form["password"]

    conn=sqlite3.connect("users.db")
    cur=conn.cursor()

    cur.execute(
        "INSERT INTO users(username,password) VALUES (?,?)",
        (username,password)
    )

    conn.commit()
    conn.close()

    return redirect("/")



# DASHBOARD

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")



# RUN CODE

@app.route("/run",methods=["POST"])
def run_code():

    data=request.get_json()

    code=data["code"]

    output=io.StringIO()

    sys.stdout=output

    try:

        exec(code)

        result=output.getvalue()

        if result=="":
            result="Program executed successfully"

    except Exception as e:

        result=str(e)

    sys.stdout=sys.__stdout__

    return jsonify({"output":result})



# SAVE FILE

@app.route("/save_file",methods=["POST"])
def save_file():

    data=request.get_json()

    filename=data["filename"]
    code=data["code"]

    conn=sqlite3.connect("users.db")
    cur=conn.cursor()

    cur.execute(
        "INSERT INTO programs(username,filename,code) VALUES (?,?,?)",
        ("demo_user",filename,code)
    )

    conn.commit()
    conn.close()

    return jsonify({"status":"saved"})



# GET FILES

@app.route("/get_files")
def get_files():

    conn=sqlite3.connect("users.db")
    cur=conn.cursor()

    cur.execute("SELECT filename,code FROM programs")

    rows=cur.fetchall()

    conn.close()

    files=[]

    for r in rows:

        files.append({
            "filename":r[0],
            "code":r[1]
        })

    return jsonify(files)



if __name__=="__main__":

    app.run(debug=True)