from flask import request, abort
from flask_restx import Namespace, Resource

ns = Namespace("data", description="receiving and sending data")

@ns.route('/send')
@ns.doc(description="Send Data to the user")
class YourResourceClass(Resource):
    def get(self):
        """
        Get method description
        """
        return {'data': 'Hello from your_namespace'}
    
@ns.route('/receive')
@ns.doc(description="Receive Data from the user")
class YourResourceClass(Resource):
    def post(self):
        """
        Create method description
        """
        return {'data': 'Hello from your_namespace'}