import json
import boto3
import time
import urllib
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('fizzbizz-bookings')

headers = {
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
}

def add_booking(event, context):
    try:
        booking_params = event['body']
        print(json.dumps(booking_params))
        booking_id   = booking_params['booking_id']
        booking_name = booking_params['booking_name']
        company      = booking_params['company']
        room_id      = booking_params['room_id']
        organizer_id = booking_params['organizer_id']
        start_time   = booking_params['start_time']
        end_time     = booking_params['end_time']
        table.put_item(
            Item = {
                'booking_id': booking_id ,
                'booking_name': booking_name,
                'room_id' : room_id,
                'company': company,
                'organizer_id': organizer_id,
                'start_time': start_time,
                'end_time': end_time
            }
        )
        status = 200
    except:
        status = 500
    finally:
        return {
            'statusCode': status,
            'headers': headers,
            'body' : {"user": username}
        }
    
def get_booking(event,context):
    try:
        params = event['pathParameters']
        booking_id = params['booking_id']
        response = table.get_item(
            Key = {
                'booking_id': booking_id
            }
        )
        booking_data = response['Item']
        status = 200
    except:
        booking_data = 'Error'
        status = 400
    finally:
        return {
            'statusCode': status,
            'headers': headers,
            'body': json.dumps(booking_data)
        }

def update_booking(event,context):
    try:
        params = event['pathParameters']
        booking_id = params['booking_id']
        response = table.get_item(
            Key = {
                'booking_id': booking_id
            }
        )
        booking_data = response['Item']
        status = 200
    except:
        booking_data = 'Error'
        status = 400
    finally:
        return {
            'statusCode': status,
            'headers': headers,
            'body': json.dumps(booking_data)
        }

def delete_booking(event,context):
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
            'headers': headers,
            'body': json.dumps(res)
        }

    

def bookings_handler(event, context):
  if event['httpMethod'] == 'POST':
    print("running add booking . . . ")
    return add_booking(event, context)
  elif event['httpMethod'] == 'GET':
    print("running get bookings . . . ")
    print(event)
    return get_booking(event, context)
  elif event['httpMethod'] == 'PUT':
    print("running update booking. . . ")
    return add_list(event, context)
  elif event['httpMethod'] == 'DELETE':
    print("running delete booking . . . ")
    print(event)
    return delete_booking(event, context)
  return {
      'statusCode': 200,
      'body': json.dumps(context)
  }
    
