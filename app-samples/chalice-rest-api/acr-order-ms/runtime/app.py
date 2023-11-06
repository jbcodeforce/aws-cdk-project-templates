import os, uuid
import boto3
from chalice import Chalice


app = Chalice(app_name='acr-order-ms')
dynamodb = boto3.resource('dynamodb')
dynamodb_table = dynamodb.Table(os.environ.get('APP_TABLE_NAME', ''))

SUPPORTED_CITIES = ['San Franciso', 'London', 'Paris', 'Berlin']


@app.route('/acr/api/v1')
def index():
    return {'health': 'good'}


@app.route('/acr/api/v1/orders', methods=['POST'])
def order():
    carRide=app.current_request.json_body
    carRide['rideID']=uuid.uuid4()
    item = {
            'PK': 'CarRide#%s' % carRide['rideID']
        }
    item.update(carRide)
    dynamodb_table.put_item(Item=item)

@app.route('/acr/api/v1/cities')
def cities():
    return {"supported_cities" : SUPPORTED_CITIES}


@app.route('/acr/api/v1/orders/{rideID}', methods=['GET'])
def get_CarRide(rideID):
    key = {
        'PK': 'CarRide#%s' % rideID
    }
    item = dynamodb_table.get_item(Key=key)['Item']
    del item['PK']
    return item
