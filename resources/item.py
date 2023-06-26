import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from db import items

blp = Blueprint("Items", "items", description="Operations on items")

# blueprint use from smorest for divide the API into multiple segment
# abort is used for good documentation instead normal return.


@blp.route("/item/<string:item_id>")
class Item(MethodView):
    def get(self, item_id):
        """List the item from items"""
        try:
            return items[item_id]
        except KeyError:
            abort(404, message="Item not found")

    def delete(self, item_id):
        """Delete the Item from Items"""
        try:
            del items[item_id]
            return {"message": "Item deleted"}
        except KeyError:
            abort(404, message="Item not found")

    def put(self, item_id):
        """update the items"""
        item_data = request.get_json()
        if "price" not in item_data or "name" not in item_data:
            abort(404, message="Bad request, Ensure 'price' and 'name' are included in JSON.")
        try:
            item = items[item_id]
            item |= item_data
            return  item
        except KeyError:
            abort(404, message="Item not found.")


@blp.route("/items")
class ItemList(MethodView):
    def get(self):
        """list the items values form items"""
        return {"stores": list(items.values())}


    def post(self):
        """Create the Item"""
        # parse the request data and load
        item_data = request.get_json()
        # if the name property is no in request data
        if "price" not in item_data or "name" not in item_data:
            abort(404, message="Bad request, Ensure 'price' and 'name' are included in JSON.")
        # lookup with store values with store name
        for item in items.values():
            if item["name"] == item_data["name"]:
                abort(400, message="the store already exist")
        # generate new store id
        item_id = uuid.uuid4().hex
        item = {**item_data, "id": item_id}
        # update the store to stores in database
        items[item_id] = item
        # return the store
        return item

