import json
import zmq

def load_catalogue():
    """
    Opens products.json and returns the data in a Python Dictionary.
    :return: Dictionary containing all product data in products.json.
    """
    try:
        with open('products.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        starter_catalogue = {'next_id': 1, 'products': []}
        save_catalogue(starter_catalogue)
        return load_catalogue()

def save_catalogue(catalogue):
    """
    Saves the input Dictionary containing updated product information to products.json.
    :param catalogue: Input Dictionary containing updated product information.
    :return: n/a
    """
    with open('products.json', 'w') as file:
        json.dump(catalogue, file, indent=4)

def add_product(new_product):
    """
    Receives a Dictionary containing new product information, parses it, and adds the new product to products.json.
    :param new_product: Dictionary containing the new product to be added to the catalogue.
    :return: String confirming success with the new product's information.
    """
    catalogue = load_catalogue()
    new_product = {
        'id': catalogue['next_id'],
        'name': new_product['name'],
        'price': new_product['price'],
        'in-stock': new_product['in-stock']
    }

    catalogue['products'].append(new_product)
    catalogue['next_id'] += 1

    save_catalogue(catalogue)
    return f'Product added: {new_product}'

def get_product(product_id):
    """
    Receives a product ID and returns the matching product record if it exists.
    :param product_id: Int representing the product ID being searched for.
    :return: JSON containing product data matching ID.
    """
    catalogue = load_catalogue()
    for product in catalogue['products']:
        if product['id'] == product_id:
            return json.dumps(product)

def edit_product(request_data):
    """
    Receives a Dictionary containing the ID of the product to edit along with the updates to be made. Updates indicated
    fields before storing the updated catalogue in products.json.
    :param request_data: Dictionary containing the ID of the product to edit along with the updates to be made.
    :return: String confirming the success of the product edit with the edited product's information.
    """
    catalogue = load_catalogue()

    # Locate product to edit and apply each update
    for product in catalogue['products']:
        if product['id'] == request_data['id']:
            for update in request_data['updates']:
                product[update] = request_data['updates'][update]

            save_catalogue(catalogue)
            return f'Product updated: {product}'

def product_report(report_type):
    """
    Parses product catalogue and returns products that match the report type.
    :param report_type: String representing what products should be returned. Options: 'all', 'in-stock',
    'out-of-stock'.
    :return: JSON object containing matching products.
    """
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
    """
    Routes the received request to the appropriate helper function and returns the resulting data.
    :param req_data: Dictionary containing the client request.
    :return: String or JSON object containing the results of the requested operation.
    """
    if req_data['type'] == 'add':
        return add_product(req_data)
    elif req_data['type'] == 'get':
        return get_product(req_data['id'])
    elif req_data['type'] == 'edit':
        return edit_product(req_data)
    elif req_data['type'] == 'report':
        return product_report(req_data['report type'])

#Setup communication (server)
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5728")


while True:
    message = socket.recv_string()
    request = json.loads(message)

    result = route_request(request)
    socket.send_string(result)