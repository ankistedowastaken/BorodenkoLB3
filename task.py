from flask import Flask, jsonify, request
from flask_httpauth import HTTPBasicAuth
import json

app = Flask(__name__)
auth = HTTPBasicAuth()

def load_data(filename):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_data(filename, data):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

users = load_data('users.json')
products = load_data('products.json')

@auth.verify_password
def verify_password(username, password):
    if username in users and users[username] == password:
        return username
    return None

@app.route('/items', methods=['GET', 'POST'])
@auth.login_required
def items():
    if request.method == 'GET':
        return jsonify(products)

    if request.method == 'POST':
        new_product = request.json
        product_id = str(len(products) + 1)
        new_product['id'] = product_id
        products[product_id] = new_product
        save_data('products.json', products)
        return jsonify(new_product), 201

@app.route('/items/<int:id>', methods=['GET', 'PUT', 'DELETE'])
@auth.login_required
def item(id):
    product = products.get(str(id))
    if not product:
        return jsonify({"error": "Product not found"}), 404

    if request.method == 'GET':
        return jsonify(product)

    if request.method == 'PUT':
        updated_product = request.json
        updated_product['id'] = str(id)
        products[str(id)] = updated_product
        save_data('products.json', products)
        return jsonify(updated_product)

    if request.method == 'DELETE':
        del products[str(id)]
        save_data('products.json', products)
        return jsonify({"message": "Product deleted"}), 200

if __name__ == '__main__':
    print("Сервер тут: http://127.0.0.1:5000/items (admin, admin)")
    app.run(debug=True)
