# Fetch Rewards Backend Challenge
## Project Overview
Our users have points in their accounts. Users only see a single balance in their accounts. But for reporting purposes we actually track their points per payer/partner. 

In our system, each transaction record contains: ​payer​ (string), ​points​ (integer), ​timestamp​ (date). For earning points it is easy to assign a payer, we know which actions earned the points. And thus which partner should be paying for the points.

When a user spends points, they don't know or care which payer the points come from. But, our accounting team does care how the points are spent. There are two rules for determining what points to "spend" first:
1. We want the oldest points to be spent first (oldest based on transaction timestamp, not the order they’re received)
2. We want no payer's points to go negative.

The web service found in this repository accepts HTTP requests to handle the following for a specific user:
- Adding transactions for a specific payer and date
- Spending points using the rules mentioned above
- Returning all payer point balances

## Tech Stack
**Language**: Python  
**API Framework**: AWS Chalice

## Development
#### Before starting, make sure you have Python and pip installed
`python --version`
`pip --version`

If you do not have Python, install latest 3.x version: 
- Official source: [python.org](https://www.python.org/)
- [Installing Python](http://docs.python-guide.org/en/latest/starting/installation/) section of _The Hitchhiker’s Guide to Python_
- Usually you will already have pip on your system or it will be included with your Python installation, otherwise: [install pip](https://pip.pypa.io/en/stable/installing/)

#### Install Pipenv packaging tool
`pip install --user pipenv`

#### Clone repository and initialize a virtual environment in the main directory
`pipenv shell`

#### Install required dependencies
`pipenv install`

#### Initialize local development environment
`cd points-web-service`  
`chalice local`

At this point you should be able to send HTTP requests locally to http://localhost:8000/. To exit the local development server use the command `CTRL+C`. 

In this directory you can also run the tests found in `/tests/test_app.py` by using the command `pytest -v`.

#### In order to deploy this service AWS credentials must be configured first
   - If AWS CLI has already been configured you can skip this step
   - Else credentials can be usually configured at `~/.aws/config` with this content:
      ```
      [default]
      aws_access_key_id=<your-access-key-id>
      aws_secret_access_key=<your-secret-access-key>
      region=<your-region>
      ```
   - More details here: [AWS Command Line Interface](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-welcome.html)

#### Once configured, deploy web service
`chalice deploy`

## Route Overview

**API URL**: http://localhost:8000/

### Add transactions for a specific payer and date

Add a single or multiple transactions for a specific payer and date. Payer and timestamp values must both be strings, with timestamp in the following format: `YYYY-MM-DDTHH:MM:SSZ`. Points values must be integers.

#### Request
`POST /transactions`
```
[
    { "payer": "DANNON", "points": 1000, "timestamp": "2020-11-02T14:00:00Z" },
    { "payer": "UNILEVER", "points": 200, "timestamp": "2020-10-31T11:00:00Z" }, 
    { "payer": "DANNON", "points": -200, "timestamp": "2020-10-31T15:00:00Z" }, 
    { "payer": "MILLER COORS", "points": 10000, "timestamp": "2020-11-01T14:00:00Z" },
    { "payer": "DANNON", "points": 300, "timestamp": "2020-10-31T10:00:00Z" }
]
```

#### Success Response
```
Status: 200 OK

[
    { "payer": "DANNON", "points": 1000, "timestamp": "2020-11-02T14:00:00Z" },
    { "payer": "UNILEVER", "points": 200, "timestamp": "2020-10-31T11:00:00Z" }, 
    { "payer": "DANNON", "points": -200, "timestamp": "2020-10-31T15:00:00Z" }, 
    { "payer": "MILLER COORS", "points": 10000, "timestamp": "2020-11-01T14:00:00Z" },
    { "payer": "DANNON", "points": 300, "timestamp": "2020-10-31T10:00:00Z" }
]
```

#### Error Responses
```
Status: 400 Bad Request

{
  "Code": "BadRequestError",
  "Message": "BadRequestError: Request body must be of type list and include at least one transaction record"
}
```

```
Status: 400 Bad Request

{
  "Code": "BadRequestError",
  "Message": "BadRequestError: Transaction records must only contain payer, points, and timestamp keys"
}
```

```
Status: 400 Bad Request

{
  "Code": "BadRequestError",
  "Message": "BadRequestError: Transaction records must contain valid data types: payer (string), points (integer), timestamp (string as YYYY-MM-DDT00:00:00Z)"
}
```

### Spend points

Spend any number of points as long as there are sufficient points in the user's balance. Points value must be of integer type.

#### Request
`POST /points`
```
{ "points": 5000 }
```

#### Success Response
```
Status: 200 OK

[
  {
    "payer": "DANNON",
    "points": -100
  },
  {
    "payer": "UNILEVER",
    "points": -200
  },
  {
    "payer": "MILLER COORS",
    "points": -4700
  }
]
```

#### Error Responses
```
Status: 400 Bad Request

{
  "Code": "BadRequestError",
  "Message": "BadRequestError: Request body must be of type dict and with a single key 'points'"
}
```

```
Status: 400 Bad Request

{
  "Code": "BadRequestError",
  "Message": "BadRequestError: Points value must be of type int"
}
```

```
Status: 409 Conflict

{
  "Error": "Not enough points available for this request",
  "Available Points": 0
}
```

### Return all payer point balances

Returns summary of points by payer. Points value must be of integer type.

#### Request
`GET /points`
```
{ "points": 5000 }
```

#### Success Response
```
Status: 200 OK

{
  "DANNON": 1000,
  "UNILEVER": 0,
  "MILLER COORS": 5300
}
```

## License
MIT
