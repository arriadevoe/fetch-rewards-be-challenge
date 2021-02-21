from chalice import Chalice

app = Chalice(app_name='points-web-service')


@app.route('/')
def index():
    return {'status': 'OK'}
