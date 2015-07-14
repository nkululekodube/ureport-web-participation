from app import app
from flask import jsonify, render_template, send_from_directory

@app.route("/register")
def register():
    return render_template('/register.html')
