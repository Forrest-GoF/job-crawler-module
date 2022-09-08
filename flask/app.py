from flask import Flask, request, jsonify
from flask_cors import CORS

from google import google_crawler
from google import url_builder
from google import validator

from dynamic import wanted_crawler
from dynamic import jumpit_crawler
from dynamic import rocketpunch_crawler
from dynamic import jobplanet_crawler

from company import nps_explorer

app = Flask(__name__)
CORS(app, supports_credentials=True)


@app.route('/')
def home():
    return "home"


@app.route('/search', methods=['GET'])
def search():
    params = request.args.to_dict()

    try:
        validator.valid_params(params)
    except Exception as e:
        raise e

    url = url_builder.bulid(params)
    data = google_crawler.crawling(url)

    return jsonify({
        "data": data,
        "length": len(data),
        "crawlingUrl": url
    })


@app.route('/wanted', methods=['GET'])
def wanted():
    params = request.args.to_dict()
    data = wanted_crawler.crawling(params["url"])
    return jsonify(data)


@app.route('/jumpit', methods=['GET'])
def jumpit():
    params = request.args.to_dict()
    data = jumpit_crawler.crawling(params["url"])
    return jsonify(data)


@app.route('/rocketpunch', methods=['GET'])
def rocketpunch():
    params = request.args.to_dict()
    data = rocketpunch_crawler.crawling(params["url"])
    return jsonify(data)


@app.route('/jobplanet', methods=['GET'])
def jobplanet():
    params = request.args.to_dict()
    data = jobplanet_crawler.crawling(params["url"])
    return jsonify(data)


@app.route('/nps', methods=['GET'])
def bass():
    params = request.args.to_dict()
    try:
        data = nps_explorer.get_bass(params["q"])
    except TypeError:
        data = []
    return jsonify({
        "data": data,
        "length": len(data)
    })


@app.route('/nps/<seq>', methods=['GET'])
def detail(seq):
    data = nps_explorer.get_detail(seq)
    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True,
            host="0.0.0.0",
            port=5000)
