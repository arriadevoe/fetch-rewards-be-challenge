from chalice import Chalice

app = Chalice(app_name='points-web-service')
app.debug = True

data_store = []


@app.route('/transaction', methods=['POST'])
def add_transaction():
    request_body = app.current_request.json_body
    data_store.append(request_body)
    return data_store


@app.route('/transactions', methods=['POST'])
def add_transaction():
    request_body = app.current_request.json_body

    if type(request_body) == list:
        for ts in request_body:
            data_store.append(request_body)
    
    return data_store


@app.route('/points', methods=['POST'])
def spend_points():
    return {'status': 'OK'}


@app.route('/points', methods=['GET'])
def get_payer_points():
    return {'status': 'OK'}