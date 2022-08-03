from flask import Flask, request, jsonify
from flask_cors import CORS

from service import crawler
from service import url_builder
from service import validator

from dynamic import wanted_crawler
from dynamic import jumpit_crawler
from dynamic import rocketpunch_crawler
from dynamic import jobplanet_crawler

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

@app.route('/test', methods=['GET'])
def test():
    params = {
        "q":"개발",
        "start":0,
        "date_posted":"",
        "employment_type":""
        }

    # url = url_builder.bulid(params)
    url = "https://www.google.com/search?vet=10ahUKEwiJ55-s4JX5AhUusJUCHXK4CQEQ06ACCKMJ..i&ei=SXLfYqfSGdbL-Qb6-onICQ&gl=kr&hl=ko&uule=w%20CAIQICILU291dGggS29yZWE&yv=3&rciv=jb&nfpr=0&chips=date_posted:today&schips=date_posted;today&q=%EA%B0%9C%EB%B0%9C&start=20&asearch=jb_list&cs=1&async=_id:VoQFxe,_pms:hts,_fmt:pc"
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