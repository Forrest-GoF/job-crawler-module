from flask import Flask, request, jsonify
from flask_cors import CORS

from service import crawler
from service import url_builder
from service import validator

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
    data = crawler.crawling(url)
    
    return jsonify({
        "data" : data,
        "length" : len(data),
        "crawling_url" : url
        })

@app.route('/test', methods=['GET'])
def test():
    params = {
        "q":"개발",
        "start":0,
        "date_posted":"",
        "employment_type":""
        }

    url = url_builder.bulid(params)
    data = crawler.crawling(url)
    
    return jsonify({
        "data" : data,
        "length" : len(data),
        "crawling_url" : url
        })

if __name__ == "__main__":
    app.run(debug=True,
            host = "0.0.0.0",
            port = 5000)