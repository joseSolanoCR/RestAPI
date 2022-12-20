import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint,abort
from db import items


blp = Blueprint("items", __name__, description="Operations in items")


@blp.route("/item/<string:item_id>")
class Store(MethodView):
    def get(self, item_id):
        try:
            return items[item_id]
        except KeyError:
            abort(404, message="Store not found")

    def delete(self, item_id):
        try:
            del items[item_id]
            return {"message": "store deleted"}
        except KeyError:
            abort(404, message="item not found")

    def put(self,item_id):
        item_data = request.get_json()
        if "price" not in item_data or "name" not in item_data:
            abort(400, message="Bad request, ensure price, store_id and name are on the JSON payload")
        try:
            item = items[item_id]
            item |= item_data
            return item
        except KeyError:
            abort(400, message="Item not found")


@blp.route("/item")
class ItemList(MethodView):
    def get(self):
        return {"items": list(items.values())}

    def post(self):
        item_data = request.get_json()
        if "name" not in item_data:
            abort(404, message="Bad request, ensure 'name' is in the JSON payload")
        for item in items.values():
            if item_data["name"] == item["name"]:
                abort(404, message="Store already exists")
        store_id = uuid.uuid4().hex
        store = {**item_data, "id": store_id}
        items[store_id] = store
        return store, 201