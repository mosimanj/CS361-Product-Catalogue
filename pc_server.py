import json
import zmq

# TODO: Add docstrings, comments

def load_catalogue():
    with open('products.json', 'r') as file:
        return json.load(file)

def save_catalogue(catalogue):
    with open('products.json', 'w') as file:
        json.dump(catalogue, file, indent=4)

def add_product(req_data):
    catalogue = load_catalogue()
    new_product = {
        'id': catalogue['next_id'],
        'name': req_data['name'],
        'price': req_data['price'],
        'in-stock': req_data['in-stock']
    }

    catalogue['products'].append(new_product)
    catalogue['next_id'] += 1

    save_catalogue(catalogue)
    return f'Product added: {new_product}'

def edit_product(req_data):
    catalogue = load_catalogue()

    for product in catalogue['products']:
        if product['id'] == req_data['id']:
            for update in req_data['updates']:
                product[update] = req_data['updates'][update]

            save_catalogue(catalogue)
            return f'Product updated: {product}'

def product_report(report_type):
    catalogue = load_catalogue()
    results = []

    if report_type == 'all':
        results = catalogue['products']
    elif report_type == 'in-stock':
        for product in catalogue['products']:
            if product['in-stock']:
                results.append(product)
    elif report_type == 'out-of-stock':
        for product in catalogue['products']:
            if not product['in-stock']:
                results.append(product)

    results = json.dumps(results)

    return results


def route_request(req_data):
    if req_data['type'] == 'add':
        return add_product(req_data)
    elif req_data['type'] == 'edit':
        return edit_product(req_data)
    elif req_data['type'] == 'report':
        return product_report(req_data['report type'])

#Setup communication (server)
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5728")


while True:
    # Receive message
    message = socket.recv_string()
    request = json.loads(message)

    result = route_request(request)
    socket.send_string(result)