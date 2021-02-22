from chalice.test import Client
from app import app


def test_transactions_missing_json():
    with Client(app) as client:
        response = client.http.get('/')
        assert response.status_code == 400
        assert response.json_body == {
            "Code": "BadRequestError",
            "Message": "BadRequestError: Error Parsing JSON"
            }

# transactions

## add transactions
    # no json object
    # empty list
    # non-list type
    # missing keys
    # wrong value types
    # single transaction
    # multiple transactions

# points

## get payer points balance

## spend points
    # no json object
    # non-numerical value
    # points key missing
    # more than one key exists
    # more points than what is available