import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.Item import ItemModel
# jwt = JWT(app, authenticate, identity)



class Item(Resource):
    parser = reqparse.RequestParser()
    # data = request.get_json(
    # #     force = True 不在乎header的格式
    # #     silent = True 不在乎header的格式 一律给出null
    # )
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="price required")

    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help="store_id required")


    @jwt_required()
    def get(self, name):

        item = ItemModel.find_by_name(name)

        if item:
            return item.json()
        # item = next(filter(lambda x: x['name'] == name, items), None)
        return {'item': item}, 200 if item else 404




    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': 'An item with name {} already exists'.format(name)}, 400
        data = Item.parser.parse_args()

        item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred inserting the item"}, 500 # internal server error

        return item.json(), 201

    def delete(self, name):
        # global items
        # items = list(filter(lambda x : x['name'] != name, items))

        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return  {'message': 'Item deleted!'}

    def put(self, name):

        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        if item is None:

            item = ItemModel(name, **data)
        else:
            item.price = data['price']

        item.save_to_db()

        return item.json()


class ItemList(Resource):
    def get(self):
        return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}
        # return {'items': [item.json() for item in ItemModel.query.all()]}