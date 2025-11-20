import zmq
import json

# Setup communication (client)
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5728")

# Example requests
add_request = {
    'type': 'add',
    'name': 'cat stickers',
    'price': 2.75,
    'in-stock': True
}

edit_request = {
    'type': 'edit',
    'id': 1,
    'updates': {'price': 3, 'in-stock': True}
}

report_request = {
    'type': 'report',
    'report type': 'out-of-stock'
}

get_request = {
    'type': 'get',
    'id': 1
}

# Example Request - Add
request_json = json.dumps(add_request)
socket.send_string(request_json)
message = socket.recv().decode('utf-8')
print(message)

# Example Request - Get
request_json = json.dumps(get_request)
socket.send_string(request_json)
message = socket.recv().decode('utf-8')
print(message)

# Example Request - Edit
request_json = json.dumps(edit_request)
socket.send_string(request_json)
message = socket.recv().decode('utf-8')
print(message)

# Example Request - Report
request_json = json.dumps(report_request)
socket.send_string(request_json)
message = socket.recv().decode('utf-8')
print(message)