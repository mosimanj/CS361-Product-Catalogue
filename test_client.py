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

# Convert request to JSON & send
request_json = json.dumps(report_request) #TODO: Add all request types
socket.send_string(request_json)

# Receive filepath and decode back to a string
message = socket.recv().decode('utf-8')
print(message)