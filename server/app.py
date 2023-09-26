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

# 1. User - POST
# - Create a User POST route by creating a class Users that inherits from Resource
# - Add the route '/users' with api.add_resource()
# - Create a POST method
# - use .get_json() to convert the request json
# - create a new user with the request data
# - add and commit the new user
# - Save the new users id to the session hash
# - Make a response and send it back to the client

# 2. Test this route in the client/src/components/Authentication.js

# 3. Create a Login route
# - Create a login class that inherits from Resource
# - Use api.add_resource to add the '/login' path
# - Build out the post method
# - convert the request from json and select the user name sent form the client.
# - Use the name to query the user with a .filter
# - If found set the user_id to the session hash
# - convert the user to_dict and send a response back to the client
# - Toggle the signup form to login and test the login route

# 4. Create an AuthorizedSession class that inherits from Resource
# - use api.add_resource to add an authorized route
# - Create a get method
# - Access the user_id from session with session.get
# - Use the user id to query the user with a .filter
# - If the user id is in sessions and found make a response to send to the client. else raise the Unauthorized exception (Note- Unauthorized is being imported from werkzeug.exceptions)

# 5. Head back to client/src/App.js to restrict access to our app!

# 6. Logout
# -  Create a class Logout that inherits from Resource
# -  Create a method called delete
# -  Clear the user id in session by setting the key to None
# -  create a 204 no content response to send back to the client

# 7. Navigate to client/src/components/Navigation.js to build the logout button!

if __name__ == "__main__":
    app.run(port=5000, debug=True)
