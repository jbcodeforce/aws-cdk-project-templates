from flask  import Flask
import boto3
from ec2_metadata import ec2_metadata

app = Flask(__name__)

@app.route('/')
def hello_world():
    client = boto3.client('ec2',ec2_metadata.region)
    rep={}
    AZs=client.describe_availability_zones()['AvailabilityZones']
    rep['Region'] = AZs[0]['RegionName']
    rep['AZs'] = AZs
    return rep


@app.route('/health')
def health():
    return "ok"


@app.route('/reverse/<string>')
def reverse(string):
    str = string[::-1]
    return  str
  

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',port=80)