from flask import Flask, request, render_template, jsonify
import numpy as np

app = Flask(__name__)

@app.route('/')
def index():
    #eturn "woos"
    return render_template("index.html")

# Login funtions
@app.route('/matrix', methods=['POST'])
def matirix():
    data = request.get_json()
    rows = int(data['rows'])
    cols = int(data['cols'])
    ans = np.random.randint(10, size=(rows,cols)).tolist
    return jsonify(ans)

if(__name__ == "__main__"):
    app.run()