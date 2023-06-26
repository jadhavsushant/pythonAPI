import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort


from db import stores

# blueprint use from smorest for divide the API into multiple segment
# abort is used for good documentation instead normal return.

blp = Blueprint("stores", __name__, description="operation on store")


@blp.route("/store/<string:store_id>")
class Store(MethodView):
    def get(self, store_id):
        try:
            return stores[store_id]
        except KeyError:
            abort(404, message="Store not found")

    def delete(self, store_id):
        try:
            del stores[store_id]
            return {"message": "Store deleted"}
        except KeyError:
            abort(404, message="Store not found")


@blp.route("/store")
class StoreList(MethodView):
    def get(self):
        return {"stores": list(stores.values())}

    def post(self):
        # parse the request data and load
        store_data = request.get_json()
        # if the name property is no in request data
        if "name" not in store_data:
            abort(400, message="The store 'name' is missing in request")
        # lookup with store values with store name
        for store in stores.values():
            if store_data["name"] == store["name"]:
                abort(400, message="the store already exist")
        # generate new store id
        store_id = uuid.uuid4().hex
        store = {**store_data, "id": store_id}
        # update the store to stores in database
        stores[store_id] = store
        # return the store
        return store

