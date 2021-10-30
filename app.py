import sqlite3

from flask import Flask, jsonify
import main

app = Flask(__name__)



@app.route('/')
def get_funds():
    assistance_program_data = main.main()
    return jsonify(assistance_program_data)


if __name__ == "__main__":
    app.run()

