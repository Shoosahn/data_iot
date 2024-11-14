from flask import Flask, jsonify
from getdata import get_data  # Pastikan namanya sesuai dengan fungsi di getdata.py


app = Flask(__name__)


@app.route('/cuaca', methods=['GET'])
def get_data_route():
    data = get_data()
    if "error" in data:
        return jsonify(data), 404
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)
