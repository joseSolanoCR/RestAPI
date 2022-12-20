import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint,abort
from db import items
from schemas import ItemSchema, ItemUpdateSchema


blp = Blueprint("items", __name__, description="Operations in items")


@blp.route("/item/<string:item_id>")
class Store(MethodView):
    @blp.response(200, ItemSchema)
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

    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id):
        try:
            item = items[item_id]
            item |= item_data
            return item
        except KeyError:
            abort(400, message="Item not found")


@blp.route("/item")
class ItemList(MethodView):
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return {"items": items.values()}

    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self,item_data):
        for item in items.values():
            if item_data["name"] == item["name"]:
                abort(404, message="Store already exists")
        store_id = uuid.uuid4().hex
        store = {**item_data, "id": store_id}
        items[store_id] = store
        return store, 201