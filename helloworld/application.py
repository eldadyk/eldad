#!flask/bin/python
import sys, os
sys.path.append(os.path.join(os.path.dirname(sys.path[0])))
import json
import requests
import boto3
import datetime

from flask import Flask, request, Response, render_template
from helloworld.flaskrun import flaskrun

application = Flask(__name__)

@application.route('/', methods=['GET'])
def get():
    return Response(json.dumps({'Output': 'Hello dor'}), mimetype='application/json', status=200)

@application.route('/get_ip', methods=['GET'])
def get_ip():
    return Response(json.dumps(get_ip_meta()), mimetype='application/json', status=200)

@application.route('/', methods=['POST'])
def post():
    return Response(json.dumps({'Output': 'Hello World'}), mimetype='application/json', status=200)

def get_ip_meta():
    user_ip = str(request.environ['REMOTE_ADDR'])
    service_url = 'http://ipinfo.io/{}'.format(user_ip) 
    return requests.get(service_url).json()
   
@application.route('/temp/<temp>', methods=['POST'])
def get_temp(temp):
    # get ip metadata from the fuction
    response = get_ip_meta()
    # create a session for boto to access the credentials that the ec2 holds
    my_ses = boto3.Session(region_name = 'us-east-2')
    # connect to the resource dynmodb using the session
    dynamodb = my_ses.resource('dynamodb')
    # refer to the table
    table = dynamodb.Table('eb_try_logger')

    item={
    'ip_addr': str(response), 
    'path': temp,
    'datetime': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    'time': datetime.datetime.now().strftime("%H:%M:%S"),
    'ip_meta' : response, # res_data
    'name':'chilkibilki'
    }
    
    print(item)
    # insert the item
    table.put_item(Item=item)
    
    return Response(json.dumps(item), mimetype='application/json', status=200)
    
  

  
    
    
    
if __name__ == '__main__':
    flaskrun(application)