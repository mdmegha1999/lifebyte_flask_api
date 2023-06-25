from flask import Flask, jsonify, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from loguru import logger
import sys
import datetime
from models import Student
from flask_cors import CORS, cross_origin

logger.add(f"{datetime.date.today()}.log")

app = Flask(__name__)
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:2010@localhost:5432/postgres"
db = SQLAlchemy(app)

logger.add(sys.stderr, format="{time} {level} {message}",
           filter="my_module", level="INFO")

# Home route that displays a welcone message


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/api')
def api_home():
    return "Welcome to API's Home"


@app.route('/api/create', methods=['POST'])
def create():
    try:
        dummy_obj = request.json
        student = Student(
            id=dummy_obj['id'],
            name=dummy_obj['name'],
            age=dummy_obj['age']
        )
        db.session.add(student)
        db.session.commit()
        db.session.close()
        # session.add(new_data)
        # session.commit()
        logger.info(f"created successfully")
        return jsonify({
            "respcode": 200,
            "process_time_ms": "",
            "result": "success"
        })
    except KeyError:
        logger.error(f"Object is not create plz try agen")
        return jsonify({
            "respcode": 400,
            "error": "Invalid request"
        }), 400
    except Exception as e:
        logger.error(f"Something went wrong {e}")
        return jsonify({
            "respcode": 500,
            "respdesc": "Internal server error"
        }), 500


@app.route('/api/data', methods=['GET'])
def read():
    students = db.session.query(Student).all()
    data = []
    for student in students:
        data.append({
            "id": student.id,
            "name": student.name,
            "age": student.age
        })
    return jsonify({"data": data})


@app.route('/api/data/<int:id>', methods=['GET'])
def get_dummy_obj(id):
    students = db.session.query(Student).get(id)
    if students:
        return jsonify({
            "id": students.id,
            "name": students.name,
            "age": students.age
        })
    else:
        return jsonify({"respcode": 404,
                        "respdesc": "data is not found"
                        }), 404


if __name__ == '__main__':
    app.run(debug=True)
