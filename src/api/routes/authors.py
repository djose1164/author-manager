from flask import Blueprint
from flask import request
from api.utils.responses import response_with
import api.utils.responses as resp
from api.models.authors import Author, AuthorSchema
from api.routes.books import book_routes
from api.models.books import Book, BookSchema
from api.utils.database import db


author_routes = Blueprint("author_routes", __name__)


@author_routes.route("/", methods=["POST"])
def create_author():
  
    data = request.get_json()
    author_schema = AuthorSchema()
    author_model = author_schema.load(data)
    print("author_model: ", author_model)
    if "books" in author_model:
        print('author_model["books"]:', author_model["books"])

    author = Author(**author_model)
    print("## Here")
    result = author_schema.dump(author.create())
    return response_with(resp.SUCCESS_201, {"author": result})



@author_routes.route("/", methods=["GET"])
def get_author_list():
    fetched = Author.query.all()
    author_schema = AuthorSchema(many=True, only=["first_name", "last_name", "id"])
    authors = author_schema.dump(fetched)
    return response_with(resp.SUCCESS_200, {"authors": authors})


@author_routes.route("/<int:author_id>", methods=["GET"])
def get_author_details(author_id):
    fetched = Author.query.get_or_404(author_id)
    author = AuthorSchema().dump(fetched)
    return response_with(resp.SUCCESS_200, {"author": author})


@author_routes.route("/<int:author_id>", methods=["PUT"])
def update_author_details(author_id):
    data = request.get_json()
    get_author = Author.query.get_or_404(author_id)
    get_author.first_name = data.get("first_name")
    get_author.last_name = data.get("last_name")
    db.session.add(get_author)
    db.session.commit()
    author = AuthorSchema().dump(get_author)
    return response_with(resp.SUCCESS_200, value={"author": author})


@author_routes.route("/<int:author_id>", methods=["PATCH"])
def modify_author_details(author_id):
    data = request.get_json()
    print("data: ", data)
    get_author = Author.query.get(author_id)
    if data.get("first_name"):
        get_author.first_name = data["first_name"]
    if data.get("last_name"):
        get_author.last_name = data["last_name"]
    db.session.add(get_author)
    db.session.commit()
    author = AuthorSchema().dump(get_author)
    return response_with(resp.SUCCESS_200, value={"author": author})


@author_routes.route("/<int:author_id>", methods=["DELETE"])
def delete_author(author_id):
    get_author = Author.query.get_or_404(author_id)
    db.session.delete(get_author)
    db.session.commit()
    return response_with(resp.SUCCESS_204)


@book_routes.route("/", methods=["GET"])
def get_book_list():
    fetched = Book.query.all()
    books = BookSchema(many=True, only=["author_id", "title", "year"]).dump(fetched)
    return response_with(resp.SUCCESS_200, value={"books": books})
