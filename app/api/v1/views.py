import re


from flask import jsonify, make_response, request
from flask_restful import Resource, request

from app.api.v1.models import IncidentsModel


class MyIncidents(Resource, IncidentsModel):
    """ Docstring for MyIncidents class, Myincidents class has
    methods for users to Create redflags(POST) and to get all red
     flag records(GET)"""

    def __init__(self):
        self.db = IncidentsModel()

    def post(self):
        """ Create a redflag """
        data = request.get_json(force=True)
        try:
            if not data:
                return make_response(jsonify({
                    "message": "No data input"
                }), 404)
            elif not data['location'] or not data["createdBy"] or not data["comment"]:
                return make_response(jsonify({
                    "data": [{"message": "Ensure you have\
    filled all fields. i.e {} " .format(data)}]
                }), 404)
        except:
            return make_response(jsonify({
                "message": "Kindly check for missing field"
            }), 404)

        createdBy = data['createdBy']
        location = data['location']
        comment = data['comment']

        if not isinstance(data['createdBy'], str) or not isinstance(data['location'], str):
            return {'message': 'Kindly input a string type'}

        if not isinstance(data['comment'], str):
            return {'message': 'Kindly input a string type'}

        if not re.match('^[a-zA-Z ]+$', createdBy):
            return {'message':
                    "CreatedBy name should be valid alphabetic characters"
                    }, 400

        if not re.match('^[a-zA-Z ]+$', location):
            return {
                'message':
                "Location name should be of valid alphabetic characters"
            }, 400

        resp = self.db.save(createdBy, location, comment)

        if resp == "white space":

            return make_response(jsonify({
                "error": "Whitespaces not allowed"
            }), 400)

        if resp == "missing data":

            return make_response(jsonify({
                "error": "Kindly input the correct data"
            })), 400

        return make_response(jsonify({
            "data": [{
                "incident_created": resp,
                "message": "Created redflag record"
            }]
        }), 201)

    def get(self):
        """ Get all red flag records """
        fetch_all = self.db.get_incidents()

        if fetch_all:

            return make_response(jsonify({
                "data": fetch_all
            }), 200)

        return make_response(jsonify({
            "error": "No Red-flag record found"
        }), 404)


class MyRecords(Resource, IncidentsModel):
    """ Docstring for MyRecords class, this class has methods that allows
    users to get specific records(GET by id), make changes to a
    record(PATCH) and to delete sepecific records(DELETE by id)"""

    def __init__(self):
        self.db = IncidentsModel()

    def get(self, id):
        """ Get a specific red-flag record """
        incidents = self.db.get_incidents()
        for i in incidents:
            if i['id'] == id:

                return make_response(jsonify({
                    "data": i
                }), 200)

        return make_response(
            jsonify(
                {
                    "error": "Redflag with that id not found"
                }
            )
        ), 404

    def delete(self, id):
        """ Allows you to delete a red-flag record """
        incidel = self.db.get_incidents()
        deleting = self.db.get_one(id)

        if not deleting:
            return {'id': id, 'message': 'Redflag not found'}, 200
        else:
            incidel.remove(deleting)

        return make_response(jsonify({
            "data": [{
                "id": id,
                "message": "red-flag record has been deleted"
            }]
        }), 200)

    def patch(self, id):
        """ Allows you to make changes to an exisiting red-flag """
        topatch = self.db.get_one(id)

        if not topatch:
            return {'message': 'Redflag to be edited not found'}, 200
        topatch.update(request.get_json())

        return make_response(jsonify({
            'data': [{
                'id': id,
                "data": topatch,
                "message": "Updated red-flag record location"
            }]
        }), 200)
