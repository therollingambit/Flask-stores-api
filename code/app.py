from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
from pkg_resources import require

from security import authenticate, identity

app = Flask(__name__)
app.secret_key = 'enaya'
api = Api(app)

jwt = JWT(app, authenticate, identity) # /auth

items = []

class Item(Resource):
  parser = reqparse.RequestParser()
  parser.add_argument('price',
    type=float,
    required=True,
    help='This field cannot be left blank!'
  )

  @jwt_required()
  def get(self, name):
    # next returns first item found by filter function
    item = next(filter(lambda x: x['name'] == name, items), None) # lambda
    return {'item': item}, 200 if item else 404

  def post(self, name):
    if next(filter(lambda x: x['name'] == name, items), None):
      return {'message': f'An item with {name} already exists.'}, 400

    data = Item.parser.parse_args()

    item = {'name': name, 'price': data['price']}
    items.append(item)
    return item, 201 # created

  def delete(self, name):
    global items
    items = list(filter(lambda x: x['name'] != name, items)) # lambda
    return {'message': f'{name} deleted'}

  def put(self, name):
    data = Item.parser.parse_args()
    item = next(filter(lambda x: x['name'] == name, items), None)

    if not item: # insert
      item = {'name': name, 'price': data['price']}
      items.append(item)
    else: # update
      item.update(data)

    return item

class ItemList(Resource):
  def get(self):
    return {'items': items}

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

app.run(port=5000, debug=True)
