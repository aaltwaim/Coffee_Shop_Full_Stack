import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
# uncomment the following line to initialize the datbase
# !! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
# !! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
# db_drop_and_create_all()

## ROUTES

@app.route('/drinks')
def get_drinks():
    try:
        drinks = Drink.query.all()
        return jsonify({
            'success':True,
            'drinks':[drink.short() for drink in drinks]
        })
    except:
        abort(404)

#  implement endpoint
#     GET /drinks
   


@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def get_drink_detail(jwt):
    try:
        drinks = Drink.query.all()
        return jsonify({
            'success':True,
            'drinks':[drink.long() for drink in drinks]
        })
    except:
        abort(404)

#  implement endpoint
#     GET /drinks-detail
    
@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def create_drink(jwt):
    body = request.get_json()
    title = body.get('title')
    recipe = body.get('recipe')

    if not('title' in body and 'recipe' in body):
        abort(422)
    try:
        drink = Drink(title=title,recipe=json.dumps(recipe))
        drink.insert()
        return jsonify({
            'success': True,
            'drinks': [drink.long()]
        })
    except:
        abort(422)

# implement endpoint
#     POST /drinks

@app.route('/drinks/<id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink(jwt, id):

    drink = Drink.query.filter(Drink.id == id).one_or_none()
    if drink:
        try:
            body = request.get_json()
            title = body.get('title')
            recipe = body.get('recipe')
            if title:
                drink.title = title
            if recipe:
                drink.recipe = recipe
            drink.update()
            return jsonify({
                'success': True,
                'drinks': [drink.long()]
            })
        except:
            abort(422)
    else:
        abort(404)



# @TODO implement endpoint
#     PATCH /drinks/<id>
     
@app.route('/drinks/<id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(jwt, id):
    drink = Drink.query.get(id)
    if drink:
        try:
            drink.delete()
            return jsonify({
                'success': True,
                'delete': id
                
            })
        except:
            abort(422)
    else:
        abort(404)


# implement endpoint
#     DELETE /drinks/<id>



## Error Handling
'''
Example error handling for unprocessable entity
'''
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
                    "success": False, 
                    "error": 422,
                    "message": "unprocessable"
                    }), 422


@app.errorhandler(404)
def not_found(error):
    return jsonify({
                    "success": False, 
                    "error": 404,
                    "message": "not found"
                    }), 404

# implement error handler for 404


@app.errorhandler(AuthError)
def auth_error_handler(ex):
    return jsonify({
                    "success": False, 
                    "error": ex.status_code,
                    "message": ex.error
                    }), 401


# implement error handler for AuthError

