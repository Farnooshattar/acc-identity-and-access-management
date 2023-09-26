from flask import request, make_response, session
from flask_restful import Resource

from models import User, Production, CrewMember

from config import app, api, db


class Productions(Resource):
    def get(self):
        production_list = [p.to_dict() for p in Production.query.all()]
        response = make_response(
            production_list,
            200,
        )

        return response

    def post(self):
        form_json = request.get_json()
        new_production = Production(
            title=form_json["title"],
            genre=form_json["genre"],
            budget=int(form_json["budget"]),
            image=form_json["image"],
            director=form_json["director"],
            description=form_json["description"],
        )

        db.session.add(new_production)
        db.session.commit()

        response_dict = new_production.to_dict()

        response = make_response(
            response_dict,
            201,
        )
        return response


api.add_resource(Productions, "/productions")


class ProductionByID(Resource):
    def get(self, id):
        production = Production.query.filter_by(id=id).first()
        if not production:
            return {"error": "Production not found"}, 404
        production_dict = production.to_dict()
        response = make_response(production_dict, 200)
        return response

    def patch(self, id):
        production = Production.query.filter_by(id=id).first()
        if not production:
            return {"error": "Production not found"}, 404

        for attr in request.form:
            setattr(production, attr, request.form[attr])

        production.ongoing = bool(request.form["ongoing"])
        production.budget = int(request.form["budget"])

        db.session.add(production)
        db.session.commit()

        production_dict = production.to_dict()

        response = make_response(production_dict, 200)
        return response

    def delete(self, id):
        production = Production.query.filter_by(id=id).first()
        if not production:
            return {"error": "Production not found"}, 404
        db.session.delete(production)
        db.session.commit()

        response = make_response("", 204)

        return response


api.add_resource(ProductionByID, "/productions/<int:id>")

# we define SignUp as a restful api, because it performs CRUD operations
# but login and authorized are not restful because they don't do CRUD


class SignUp(Resource):
    def post(self):
        data = request.get_json()
        user = User(
            name=data["name"],
            email=data["email"]
        )
        db.session.add(user)
        db.session.commit()

        session["user_id"] = user.id
        return user.to_dict(), 200


api.add_resource(SignUp, "/signup")


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    user = User.query.filter(User.name == data["name"]).first()

    session["user_id"] = user.id
    return user.to_dict(), 200


@app.route("/authorized", methods=["GET"])
def authorized():
    user = User.query.filter(User.id == session.get("user_id")).first()
    print(user)
    if user:
        return user.to_dict(), 200
    else:
        return {"errors": "unauthorized"}, 401


if __name__ == "__main__":
    app.run(port=5000, debug=True)
