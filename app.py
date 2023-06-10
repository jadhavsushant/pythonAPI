from flask import Flask, jsonify, request

app = Flask(__name__)

stores = [{"name": "my store", "items": [{"name": "chair", "price": 99}]}]


@app.get("/store")
def get_stores():
    return {"stores": stores}


@app.post("/store")
def create_store():
    request_data = request.get_json()
    new_store = {"name": request_data["name"], "items": []}
    stores.append(new_store)
    return new_store, 201


@app.post("/store/<string:name>/item")
def create_item(name):
    requested_data = request.get_json()
    for store in stores:
        if store["name"] == name:
            new_item = {
                "name": requested_data["name"],
                "price": requested_data["price"],
            }
            store["items"].append(new_item)
            return new_item, 201
    return {"Error": "Store not found"}, 404


@app.get("/store/<string:name>")
def get_store(name):
    for store in stores:
        if store["name"] == name:
            return store
    return {"Error": "Store not found"}, 404


@app.get("/store/<string:name>/item")
def get_store_items(name):
    for store in stores:
        if store["name"] == name:
            return {"Items" : store["items"]}
    return {"Error": "Store not found"}, 404

if __name__ == "__main__":
    app.run(debug=True)
