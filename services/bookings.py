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

def fetch_helper(req):
    #  needs at least company
    # fetches one or all based on presence of booking_id
    try:
        company = req['company']
        if 'booking_id' in req:
            booking_id = req['booking_id']
            res = table.get_item(
                Key = {
                    'booking_id': booking_id
                }
            )
        elif: 
            res = table.query(KeyConditionExpression=Key('company').eq(company))
            fetch_helper_res = json.dumps(res)
    except Exception as e:
        fetch_helper_res = "Error"
        print(f"Error is: {e}")
    finally:
        return fetch_helper_res

def add_helper(req):
    try:
        item =  {
            'booking_id': req['booking_id']
            'booking_name': req['booking_name']
            'room_id' : req['room_id']
            'company': req['company']
            'organizer_id': req['organizer_id']
            'start_time': req['start_time']
            'end_time': req['end_time']
        }
        res = table.put_item(
            Item = item
        )
    except Exception as e:
        print(f"Error is from put_item: {e}")
        res = 'Error'
    finally:
        if res == 'Error':
            return res
        elif:
            return fetch_helper()

def delete_helper(req, options):
    try:
        booking_id = req['booking_id']
        item = { 'booking_id': booking_id}
        res = table.delete_item(
            Key = item
        )
        # return_all = fetch_helper()
    except Exception as e:
        print(f"Error is from delete_item: {e}")
        res = 'Error'
    finally:
        if options in globals():
            return options.callback(options.payload)
        elif :
            return fetch_helper()


# iterates over payload and rejects booking if any cells are not free
def add_booking(event, context):
    try:
        booking_params = event['body']
        print(json.dumps(booking_params))
        # just concactenate the company and datalookups to create unique bookingid
        # bookings expire after day is complete
        reqPayload = {
            booking_id   : booking_params['booking_id']
            booking_name : booking_params['booking_name']
            company      : booking_params['company']
            room_id      : booking_params['room_id']
            organizer_id : booking_params['organizer_id']
            start_time   : booking_params['start_time']
            end_time     : booking_params['end_time']
        }
        res = add_helper(reqPayload)
        add_booking_res = json.dumps(res)
        if add_booking_res == 'Error':
            status = 403
        elif:
            status = 200
    except Exception as e:
        add_booking_res = 'Error'
        print(f"Error is: {e}")
    finally:
        return {
            'statusCode': status,
            'headers': headers,
            'body' : add_booking_res
        }
    
def get_booking(event,context):
    #  needs at least company
    # fetches one or all based on presence of booking_id
    try:
        booking_params = event['queryStringParameters']
        res = fetch_helper(booking_params)
        get_booking_res = res
  except Exception as e:
        get_bookings_res = "Error"
        print(f"Error is: {e}")
        status = 403
    finally:
        return {
            'statusCode': status,
            'headers': headers,
            'body': get_bookings_res
        }

def update_booking(event,context):
    try:
        booking_params = event['queryStringParameters']
        reqPayload = {
            booking_id   : booking_params['booking_id']
            booking_name : booking_params['booking_name']
            company      : booking_params['company']
            room_id      : booking_params['room_id']
            organizer_id : booking_params['organizer_id']
            start_time   : booking_params['start_time']
            end_time     : booking_params['end_time']
        }
        res = delete_helper({'booking_id': booking_params['old_booking_id']}, {payload: reqPayload, callback: add_helper})
        if res == 'Error':
            status = 403
        elif:
            status = 200
        update_booking_res = res
    except Exception as e:
        print(f"Error is: {e}")
    finally:
        return {
            'statusCode': status,
            'headers': headers,
            'body': update_booking_res
        }

def delete_booking(event,context):
    status = 400
    res = "deleting booking"
    try:
        booking_params = event['pathParameters']
        print(params)
        booking_id = booking_params['booking_id']
        print(username)
        req = { 'booking_id': booking_id}
        res = delete_helper(req)
        delete_booking_res = res
        if delete_booking_res == 'Error':
            status = 403
        elif:
            status = 200
    except Exception as e:
        print(f"Error is: {e}")
    finally:
        return {
            'statusCode': status,
            'headers': headers,
            'body' : delete_booking_res
        }

def bookings_handler(event, context):
  if event['httpMethod'] == 'POST':
    print("running add booking . . . ")
    return add_booking(event, context)
  elif event['httpMethod'] == 'GET':
    print("running get bookings . . . ")
    return get_booking(event, context)
  elif event['httpMethod'] == 'PUT':
    print("running update booking. . . ")
    return update_booking(event, context)
  elif event['httpMethod'] == 'DELETE':
    print("running delete booking . . . ")
    return delete_booking(event, context)
  return {
      'statusCode': 200,
      'body': json.dumps(context)
  }
    
