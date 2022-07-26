from unittest import result
from flask import Blueprint, request
from api.utils.responses import response_with
import api.utils.responses as resp
from api.utils.database import db
from api.models.users import User, UserSchema

user_routes = Blueprint("user_routes", __name__)


@user_routes.route("/", methods=["POST"])
def create_user():
    try:
        data = request.get_json()
        data["password"] = User.generate_hash(data["password"])
        user_schema = UserSchema()
        user = user_schema.load(data)
        return response_with(
            resp.SUCCESS_200, value={"user": user_schema.dump(user.create())}
        )
    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)

@user_routes.route("/login", methods=["POST"])
def authenticate_user():
    data = request.get_data()
    current = User.find_user_by_username(data["username"])