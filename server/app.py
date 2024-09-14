from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api, Resource
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)

@app.route('/example', methods=['GET', 'POST'])
def examples():
    if request.method == 'GET':
        examples = Example.query.all()
        return make_response(
            jsonify([example.to_dict() for example in examples]),
            200,
        )
    elif request.method == 'POST':
        data = request.get_json()
        hire_date = datetime.strptime(data.get('hire_date'), '%Y-%m-%d')
        new_example = Example(
            name=data.get('name'),
            hire_date=hire_date,
            manager_id=data.get('manager_id'),
        )
        db.session.add(new_example)
        db.session.commit()
        return make_response(new_example.to_dict(), 201)
        
    return make_response(
        jsonify({'text': 'Method not Allowed'}),
        405,
    )

@app.route('/examples/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def example_by_id(id):
    example = Example.query.filter(Example.id == id).first()
    
    if example is None:
        response_body = {
            "message": "This example does not exist in our database. Please try again."
        }
        response = make_response(response_body, 404)
        return response

    elif request.method == 'GET':
        response = make_response(example.to_dict(), 200)
        return response
    
    elif request.method == 'PATCH':
        data = request.get_json()
        if 'name' in data:
            example.name = data['name']
        db.session.add(example)
        db.session.commit()
        response = make_response(example.to_dict(), 200)
        return response
    
    elif request.method == 'DELETE':
        db.session.delete(example)
        db.session.commit()

        response_body = {
            "delete_successful": True,
            "message": "Example deleted."
        }

        response = make_response(response_body, 200)
        return response