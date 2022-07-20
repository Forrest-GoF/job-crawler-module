from flask import Flask, request, jsonify
from flask_cors import CORS

from service import crawler

app = Flask(__name__) 
CORS(app, supports_credentials=True,
 resources={r'*': {'origins': 'http://localhost:3000'}})

@app.route('/')
def home():
    return "home"

@app.route('/search', methods=['GET'])
def search():
    params = request.args.to_dict()
    
    url = crawler.build_url(params)
    data = crawler.crawling(url)
    
    return jsonify({
        "data" : data,
        "crawling_url" : url
        })

if __name__ == "__main__":
    app.run(debug=True,
            host = "0.0.0.0",
            port = 5000)
    