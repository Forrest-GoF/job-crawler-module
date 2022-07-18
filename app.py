from crawler import crawling
from flask import Flask, jsonify, request
from flask_restx import Resource, Api

app = Flask(__name__)
api = Api(app)

@api.route('/search')
class Api(Resource):
    def get(self):
        q = request.args.get('q')
        start = request.args.get('start')
        date_posted = request.args.get('date_posted')
        employment_type = request.args.get('employment_type')

        job_previews = crawling(q, start,date_posted,employment_type)

        return jsonify({"data":job_previews})

if __name__ == '__main__':
    app.run(debug=True, port=5002)
