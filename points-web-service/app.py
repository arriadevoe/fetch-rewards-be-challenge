from chalice import Chalice

app = Chalice(app_name='points-web-service')
app.debug = True
data_store = {}

@app.route('/')
def index():
    return {'status': 'OK'}

@app.route('/points', methods=['GET'])
def get_payer_points():
    return {'status': 'OK'}

@app.route('/points', methods=['POST'])
def spend_points():
    return {'status': 'OK'}

@app.route('/transaction', methods=['POST'])
def add_transaction():
    return {'status': 'OK'}