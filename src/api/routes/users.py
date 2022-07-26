from crypt import methods
from unittest import result
from flask import Blueprint, request
from flask_jwt_extended import create_access_token
from api.utils.responses import response_with
import api.utils.responses as resp
from api.utils.database import db
from api.models.users import User, UserSchema
from api.utils.token import confirm_verification_token

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
    try:
        data = request.get_json()
        current_user = None

        if data.get("email"):
            current_user = User.find_user_by_email(data["email"])
        elif data.get("username"):
            current_user = User.find_user_by_username(data["username"])

        if not current_user:
            return response_with(resp.SERVER_ERROR_404)
        if not current_user.is_verified:
            return response_with(resp.BAD_REQUEST_400)

        if User.verify_hash(data["password"], current_user.password):
            access_token = create_access_token(identity=data["username"])
            return response_with(
                resp.SUCCESS_201,
                value={
                    "message": f"Logged in as {current_user.username}",
                    "access_token": access_token,
                },
            )
        else:
            response_with(resp.UNAUTHORIZED_401)
    except Exception as e:
        print(f"## {e}")
        return response_with(resp.INVALID_INPUT_422)

user_routes.route("/confirm/<token>", methods=["GET"])
def verify_email(token):
    try:
        email = confirm_verification_token(token)
    except Exception:
        return response_with(resp.SERVER_ERROR_500)
    user = User.query.filter_by(email=email).first()
    if user.is_verified:
        return response_with(resp.INVALID_INPUT_422)
    else:
        user.is_verified = True
        db.session.add(user)
        db.session.commit()
        return response_with(resp.SUCCESS_200, value={
            "message": "Email verified, you can process to login now."
        })
    
