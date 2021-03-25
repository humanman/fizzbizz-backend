import json
import boto3
import time
import urllib
import uuid
# from cryptoaddress import EthereumAddress()
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('fizzbizz-users')

# def corshandler():
#     corsOrigin = DEFAULT_ORIGIN; // default value
#     const inputOrigin = R.path(['headers','origin'], event);

#     if (R.test(ORIGIN_PATTERN, inputOrigin)) {
#       corsOrigin = inputOrigin;
#     }
    


headers = {
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Allow-Origin': 'http://unkempt-advice.surge.sh',
    'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
}

def add_user(event, context):
    # TODO: ENCRYPT/DECRYPT email
    try:
        user_params = json.loads(event['body'])
        print(json.dumps(user_params))
        username  =  'web3User'
        email = 'web3User'
        if 'username' in user_params:
            username  = user_params['username']
        if 'email' in user_params:
            email = user_params['email']
        publicAddr  = user_params['pubAddr']
        # create nonce every time
        nonce     = uuid.uuid4().hex
        company  = user_params['company']
        table.put_item(
            Item = {
                'nonce': nonce,
                'username': username,
                'email': email,
                'pubAddr': publicAddr,
                'company': company,
                # 'bookings': []
            }
        )
        status = 200
    except Exception as e:
        print(f"Error is: {e}")
        status = 403
    finally:
        return {
            'statusCode': status,
            'headers': headers,
            'body' : json.dumps(str({
                "user": username,
                "nonce": nonce
                }))
        }
    
def get_user(event,context):
    try:
        params   = event['queryStringParameters']
        pubAddr  = params['pubAddr']
        company = params['company']
        res = table.get_item(
            Key = {
                'pubAddr': pubAddr,
                'company': company
            }
        )
        print(res)
        if 'Item' in res:
            status = 200
            get_user_res = json.dumps(res['Item'])
        else:
            get_user_res = 'new user'
            status = 403
    except Exception as e:
        get_user_res = "Error"
        print(f"Error is: {e}")
        status = 403
    finally:
        print(get_user_res)
        return {
            'statusCode': 200,
            'headers': headers,
            'body': get_user_res
        }

def update_user(event,context):
    try:
        params = event['pathParameters']
        username = params['username']
        update_user_res = table.put_item(
            Key = {
                'username': username
            }
        )
        status = 200
    except Exception as e:
        update_user_res = 'Error'
        print(f"Error is: {e}")
        status = 400
    finally:
        return {
            'statusCode': status,
            'headers': headers,
            'body': json.dumps(update_user_res)
        }


def delete_user(event,context):
    status = 400
    try:
        params = event['pathParameters']
        print(params)
        username = params['username']
        print(username)
        delete_user_res = table.delete_item(
            Key = {
                'username': username
            }
        )
        status = 200
    except Exception as e:
        status = 400
        delete_user_res = 'Error'
        print(f"Error is: {e}")
    finally:
        return {
            'statusCode': status,
            'headers': headers,
            'body': json.dumps(res)
        }

    

def users_handler(event, context):
  if event['httpMethod'] == 'POST':
    print("running add user . . . ")
    return add_user(event, context)
  elif event['httpMethod'] == 'GET':
    print("running get user . . . ")
    print(event)
    return get_user(event, context)
  elif event['httpMethod'] == 'PUT':
    print("running update user . . . ")
    return update_user(event, context)
  elif event['httpMethod'] == 'DELETE':
    print("running delete user . . . ")
    print(event)
    return delete_user(event, context)
  return {
      'statusCode': 200,
      'body': json.dumps(context)
  }
    
