from flask import Flask, request, jsonify

from service import crawler

app = Flask(__name__) 

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
    app.run(debug=True)
    