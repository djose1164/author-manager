from unittest import result
from flask import Blueprint, request
from api.utils.responses import response_with
import api.utils.responses as resp
from api.models.books import Book, BookSchema
from api.utils.database import db


book_routes = Blueprint("book_routes", __name__)


@book_routes.route("/", methods=["POST"])
def create_book():
    try:
        data = request.get_json()
        book = Book(data["title"], data["year"], author_id=data["author_id"])
        result = BookSchema().dump(book.create())
        return response_with(resp.SUCCESS_201, value={"book": result})
    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)


@book_routes.route("/<int:id>", methods=["GET"])
def get_book_detail(id):
    fetched = Book.query.get_or_404(id)
    book = BookSchema().dump(fetched)
    return response_with(resp.SUCCESS_200, value={"book": book})


@book_routes.route("/<int:id>", methods=["PUT"])
def update_book_detail(id):
    data = request.get_json()
    get_book = Book.query.get_or_404(id)
    get_book.title = data["title"]
    get_book.year = data["year"]
    db.session.add(get_book)
    db.session.commit()
    return response_with(resp.SUCCESS_200, value={"book": BookSchema.dump(get_book)})


@book_routes.route("/<int:id>", methods=["PATCH"])
def modify_book_detail(id):
    get_book = Book.query.get_or_404(id)
    data = request.get_json()
    if data.get("title"):
        get_book.title = data["title"]
    if data.get("year"):
        get_book.year = data["year"]
    db.session.add(get_book)
    db.session.commit()
    return response_with(resp.SUCCESS_200, value={"book": BookSchema().dump(get_book)})


@book_routes.route("/<int:id>", methods=["DELETE"])
def delete_book(id):
    get_book = Book.query.get_or_404(id)
    db.session.delete(get_book)
    db.session.commit()
    return response_with(resp.SUCCESS_204)