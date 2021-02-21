from itertools import chain 
from chalice import Chalice, BadRequestError

app = Chalice(app_name='points-web-service')
app.debug = True

data_store = []


@app.route('/transactions', methods=['POST'])
def add_transaction():
    request_body = app.current_request.json_body

    if type(request_body) == list:
        temp_store = []

        for transaction in request_body:
            if set(transaction.keys()) == {"payer", "points", "timestamp"}:
                temp_store.append(transaction)            
            else:
                raise BadRequestError("Transaction records must contain payer (string), points (integer), and timestamp (date)")

        data_store.extend(temp_store)
    else:
        raise BadRequestError("Request body must be of type list")
    
    return data_store


@app.route('/points', methods=['POST'])
def spend_points():
    return {'status': 'OK'}


@app.route('/points', methods=['GET'])
def get_payer_points():
    return {'status': 'OK'}