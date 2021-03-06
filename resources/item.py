# import sqlite3
from flask_restful import Resource,reqparse
# from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required = True,
        help = "This field cannot be left blank")
    parser.add_argument('store_id',
        type=int,
        required = True,
        help = "Every item needs a store id.")
    
#    @jwt_required()
    def get(self,name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message' : 'Item not found'}, 404 

    
    def post(self,name):
        if ItemModel.find_by_name(name):
            return {'message': "An item with name {} already exists".format(name)}, 400
        
        data = Item.parser.parse_args()   #This is bcoz we are sending item name to be created in URL and price from JSON body so we need to get that body from API (Payload)
        # data = request.get_json()

        item = ItemModel(name,data['price'],data['store_id'])     #can be simplified as item = ItemModel(name, **data) **data then unpacks to data['price'] and data['store_id']

        try:
            item.save_to_db()
        except:
            return {"message":"An error occured inserting the item"} ,500  #Internal Server Error
        return item.json(), 201


    def delete(self,name):
        item = ItemModel.find_by_name(name)
        if(item):
            item.delete_from_db()

        return {'message': 'Item Deleted'}


    def put(self,name):
        data = Item.parser.parse_args()

        # data = request.get_json()
        item = ItemModel.find_by_name(name)
        # updated_item = ItemModel(name, data['price'])
        if item is None:
            item = ItemModel(name,data['price'],data['store_id'])
            # try:
            #     updated_item.insert()
            # except:
            #     return {"message" : "An error occured inserting the item"}, 500
        else:
            # try:
            #     updated_item.update()
            # except:
            #     return {"message" : "An error occured updating the item"}, 500
            item.price = data['price']

        item.save_to_db()

        return item.json()


class ItemList(Resource):
    def get(self):
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()

        # query = "SELECT * FROM items"
        # result = cursor.execute(query)
        # items = []
        # for row in result:
        #     items.append({'name':row[0],'price':row[1]})

        # connection.close()
        # return {'items' : items}
        return {'items' : [x.json() for x in ItemModel.query.all()]}
        #return {'items' : list(map(lambda x: x.json(), ItemModel.query.all()))}    Using lambda function
