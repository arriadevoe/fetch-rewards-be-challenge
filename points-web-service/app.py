from itertools import chain 
from chalice import Chalice, BadRequestError, Response

app = Chalice(app_name='points-web-service')
app.debug = True

transaction_store = []

def custom_error(msg, status):
    return Response(
        body={"error": msg},
        headers={'Content-Type': 'text/plain'},
        status_code=status
        ) 


@app.route('/transactions', methods=['POST'])
def add_transaction():
    req_transaction_list = app.current_request.json_body

    if type(req_transaction_list) == list:
        for transaction in req_transaction_list:
            if set(transaction.keys()) != {"payer", "points", "timestamp"}:
                raise BadRequestError("Transaction records must contain payer (string), points (integer), and timestamp (date)")

        transaction_store.extend(req_transaction_list)
    else:
        raise BadRequestError("Request body must be of type list with at least one transaction record")
    
    return transaction_store


@app.route('/points', methods=['GET'])
def get_payer_points():
    point_balances = {}

    for transactions in transaction_store:
        curr_payer = transactions['payer']
        if curr_payer in point_balances.keys():
            point_balances[curr_payer] += int(transactions['points'])
        else:
            point_balances[curr_payer] = int(transactions['points'])

    return point_balances


@app.route('/points', methods=['POST'])
def spend_points():
    global transaction_store
    request_body = app.current_request.json_body
    sorted_transactions = sorted(
        transaction_store,
        key = lambda ts: ts['timestamp']
        )
    
    points_to_spend = request_body['points']
    points_spent = {}

    total_points_available = sum([ts['points'] for ts in sorted_transactions])
    if points_to_spend > total_points_available:
        return custom_error("no more points to spend", 400)
        
    for ts_idx, transaction in enumerate(sorted_transactions):
        ts_points = transaction['points']
        if points_to_spend > 0 and ts_points != 0:
            if points_to_spend >= ts_points:
                points_consumed = ts_points
                points_to_spend -= points_consumed
                sorted_transactions[ts_idx]['points'] = 0
            else:
                points_consumed = points_to_spend
                ts_remainder = ts_points - points_consumed
                sorted_transactions[ts_idx]['points'] = ts_remainder
                points_to_spend = 0

            ts_payer = transaction['payer']

            if ts_payer in points_spent.keys():
                points_spent[ts_payer] += points_consumed
            else:
                points_spent[ts_payer] = points_consumed
        elif points_to_spend == 0:
            break
    
    transaction_store = sorted_transactions
    points_spent_resp = [{'payer': payer, 'points': -points} for payer, points in points_spent.items()]

    return points_spent_resp
