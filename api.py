from flask import Flask, jsonify, request
from flask_restx import Resource, Api

import crawler

app = Flask(__name__)
api = Api(app)

@api.route('/search')
class Api(Resource):
    def get(self):
        params = request.args.to_dict()

        url = crawler.build_url(params)
        data = crawler.crawling(url)
        
        return jsonify({
            "data" : data,
            "data_length" : len(data),
            "url" : url
            })

if __name__ == '__main__':
    app.run(debug=True, port=5002)
