from flask import Flask, jsonify
from flask_restx import Resource, Api
from flask_swagger_ui import get_swaggerui_blueprint
import receive_api

app = Flask(__name__)
api = Api(app, version='1.0', title='FixIt', description='API documentation')

# Include your test_api namespace from the test_api.py file
api.add_namespace(receive_api.ns)

if __name__ == '__main__':
    app.run(debug=True)