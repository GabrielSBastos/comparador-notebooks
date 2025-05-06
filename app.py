
from flask import Flask, jsonify, render_template
import json
from flask_cors import CORS

app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/detalhes.html')
def detalhes():
    return render_template("detalhes.html")

@app.route('/api/dados')
def dados():
    with open("dados.json", "r", encoding="utf-8") as f:
        produtos = json.load(f)
    for p in produtos:
        p["historico"] = [p["valor"], "R$ 3299,00", "R$ 3199,00"]
    return jsonify(produtos)

if __name__ == '__main__':
    app.run(debug=True)
