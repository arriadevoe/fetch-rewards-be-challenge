from itertools import chain 
from chalice import Chalice, BadRequestError, Response

app = Chalice(app_name='points-web-service')
app.debug = True

transaction_store = []

def custom_error(body, status):
    return Response(
        body=body,
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
    
    requested_points = request_body['points']
    total_points_available = sum([ts['points'] for ts in sorted_transactions])
    
    if requested_points > total_points_available:
        error_dict = {
            "Error": "Not enough points available for this request",
            "Available Points": total_points_available
        }
        return custom_error(error_dict, 400)
    
    points_spent = {}
        
    for ts_idx, transaction in enumerate(sorted_transactions):
        ts_points = transaction['points']
        if requested_points > 0 and ts_points != 0:
            if requested_points >= ts_points:
                points_consumed = ts_points
                requested_points -= points_consumed
                sorted_transactions[ts_idx]['points'] = 0
            else:
                points_consumed = requested_points
                ts_remainder = ts_points - points_consumed
                sorted_transactions[ts_idx]['points'] = ts_remainder
                requested_points = 0

            ts_payer = transaction['payer']

            if ts_payer in points_spent.keys():
                points_spent[ts_payer] += points_consumed
            else:
                points_spent[ts_payer] = points_consumed
        elif requested_points == 0:
            break
    
    transaction_store = sorted_transactions
    points_spent_resp = [{'payer': payer, 'points': -points} for payer, points in points_spent.items()]

    return points_spent_resp
