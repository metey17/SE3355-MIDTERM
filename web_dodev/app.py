from flask import Flask, render_template, request, jsonify
import json
from collections import Counter

app = Flask(__name__, static_url_path='/')


@app.route('/')
def index():
    return render_template('index.htm')


@app.route('/api/search', methods=['GET'])
def api_search_products():
    query = request.args.get('q')
    size = request.args.get('s')
    price_order = request.args.get('p')
    category = request.args.get('c')

    with open('database/products.json', 'r', encoding='utf-8') as file:
        products = json.load(file)

    filtered_products = products

    if query:
        filtered_products = [product for product in filtered_products if query.lower(
        ) in product['name'].lower()]

    if category:
        categories = [cat.strip().lower() for cat in category.split(',')]
        filtered_products = [product for product in filtered_products if any(
            cat in product['category'].lower().split(', ') for cat in categories)]

    if size:
        filtered_products = [
            product for product in filtered_products if size.lower() in product['size'].lower()]

    if price_order == '0':
        filtered_products = sorted(filtered_products, key=lambda x: x['price'])
    elif price_order == '1':
        filtered_products = sorted(
            filtered_products, key=lambda x: x['price'], reverse=True)

    category_list = [cat.strip(
    ) for product in filtered_products for cat in product['category'].split(',')]
    category_counter = Counter(category_list)
    category_result = {category: quantity for category,
                       quantity in category_counter.items()}

    _category_list = []
    for cat in category_list:
        if cat not in _category_list:
            _category_list.append(cat)

    result = {
        "result": filtered_products,
        "category": _category_list,
        "category_quantity": category_result
    }

    return jsonify(result)


@app.route('/detail/<int:product_id>', methods=['GET'])
def product_detail(product_id):
    with open('database/products.json', 'r', encoding='utf-8') as file:
        products = json.load(file)

    product = next(
        (product for product in products if product['id'] == product_id), None)

    if product:
        return render_template('detail.htm', product=product)
    else:
        return render_template('404.htm'), 404


@app.route('/search', methods=['GET'])
def search_products():
    query = request.args.get('q')
    size = request.args.get('s')
    price_order = request.args.get('p')
    category = request.args.get('c')

    with open('database/products.json', 'r', encoding='utf-8') as file:
        products = json.load(file)

    filtered_products = products

    if query:
        filtered_products = [product for product in filtered_products if query.lower(
        ) in product['name'].lower()]

    if category:
        categories = [cat.strip().lower() for cat in category.split(',')]
        filtered_products = [product for product in filtered_products if any(
            cat in product['category'].lower().split(', ') for cat in categories)]

    if size:
        filtered_products = [
            product for product in filtered_products if size.lower() in product['size'].lower()]

    if price_order == '0':
        filtered_products = sorted(filtered_products, key=lambda x: x['price'])
    elif price_order == '1':
        filtered_products = sorted(
            filtered_products, key=lambda x: x['price'], reverse=True)
    else:
        price_order = '0'
        filtered_products = sorted(filtered_products, key=lambda x: x['price'])

    category_list = [cat.strip(
    ) for product in filtered_products for cat in product['category'].split(',')]
    category_counter = Counter(category_list)
    category_result = {category: quantity for category,
                       quantity in category_counter.items()}

    _category_list = []
    for cat in category_list:
        if cat not in _category_list:
            _category_list.append(cat)

    result = {
        "result": filtered_products,
        "category": _category_list,
        "category_quantity": category_result
    }

    return render_template('search.htm', products=result, param={"q": query, "p": price_order, "c": category, "s": size})


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.htm'), 404


if __name__ == '__main__':
    app.run(debug=True)
