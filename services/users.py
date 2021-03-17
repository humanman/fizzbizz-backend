import json
import boto3
import time
import urllib
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('fizzbizz-users')

def add_user(event, context):
    try:
        user_params = event['body']
        print(json.dumps(user_params))
        # should check for `username` and only add legal stuff instead of all params
        username = user_params['username']
        email = user_params['email']
        table.put_item(
            Item = {
                'username': username ,
                'email': email,
                'lists': ['1']
            }
        )
        status = 200
    except:
        status = 500
    finally:
        return {
            'statusCode': status,
            'body' : {"user": username}
        }
    
def get_user(event,context):
    try:
        params = event['pathParameters']
        username = params['username']
        response = table.get_item(
            Key = {
                'username': username
            }
        )
        user_data = response['Item']
        status = 200
    except:
        user_data = 'Error'
        status = 400
    finally:
        return {
            'statusCode': status,
            'body': json.dumps(user_data)
        }

def update_user(event,context):
    try:
        params = event['pathParameters']
        username = params['username']
        response = table.get_item(
            Key = {
                'username': username
            }
        )
        user_data = response['Item']
        status = 200
    except:
        user_data = 'Error'
        status = 400
    finally:
        return {
            'statusCode': status,
            'body': json.dumps(user_data)
        }


def delete_user(event,context):
    status = 400
    res = "deleting user"
    try:
        params = event['pathParameters']
        print(params)
        username = params['username']
        print(username)
        response = table.delete_item(
            Key = {
                'username': username
            }
        )
        status = 200
        res = response
    except Exception as e:
        status = 400
        res = e
        print(e)
    finally:
        return {
            'statusCode': status,
            'body': json.dumps(res)
        }

    

def users_handler(event, context):
  if event['httpMethod'] == 'POST':
    print("running add user . . . ")
    return add_user(event, context)
  elif event['httpMethod'] == 'PUT':
    print("running add list . . . ")
    return add_list(event, context)
  elif event['httpMethod'] == 'GET':
    print("running get lists . . . ")
    print(event)
    return get_user(event, context)
  elif event['httpMethod'] == 'DELETE':
    print("running delete user . . . ")
    print(event)
    return delete_user(event, context)
  return {
      'statusCode': 200,
      'body': json.dumps(context)
  }
    
