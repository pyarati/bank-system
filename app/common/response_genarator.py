from flask_restful import Resource
from flask import jsonify, make_response


class ResponseGenerator(Resource):
    def __init__(self, data, message, success, status):
        self.data = data
        self.message = message
        self.success = success
        self.status = status

    def success_response(self):
        response = {"data": self.data,
                    "message": self.message,
                    "success": self.success,
                    "status": self.status}
        return make_response(jsonify(response), self.status)

    def error_response(self):
        response = {"data": self.data,
                    "message": self.message,
                    "success": self.success,
                    "status": self.status}
        return make_response(jsonify(response), self.status)
