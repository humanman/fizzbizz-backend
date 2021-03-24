import json
import boto3
import time
import urllib
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key

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
    print(req)
    try:
        company = req['company']
        # if 'booking_id' in req:
        #     booking_id = req['booking_id']
        #     res = table.get_item(
        #         Key = {
        #             'booking_id': booking_id,
        #             'company'   : company
        #         }
        #     )
            # no use case for just one yet
            # this method will always fetch all filtered by company
            # print(json.dumps(single_get)
        res = table.scan(FilterExpression=Key('company').eq(company))
        fetch_helper_res = str(res["Items"])
        # print(fetch_helper_res)
    except Exception as e:
        fetch_helper_res = "Error"
        print(f"Error is from fetch_helper: {e}")
    finally:
        return fetch_helper_res

def add_helper(req):
    company = req['company']
    res = None
    try:
        item =  {
            'booking_id': req['booking_id'],
            'booking_name': req['booking_name'],
            'room_id' : req['room_id'],
            'company': company,
            'organizer_id': req['organizer_id'],
            'start_time': req['start_time'],
            'end_time': req['end_time']
        }
        res = table.put_item(
            Item = {
                'booking_id': req['booking_id'],
                'booking_name': req['booking_name'],
                'room_id' : req['room_id'],
                'company': company,
                'organizer_id': req['organizer_id'],
                'start_time': req['start_time'],
                'end_time': req['end_time']
            }
        )
    except Exception as e:
        print(f"Error is from add_helper: {e}")
        res = 'Error'
    finally:
        if res == 'Error':
            return res
        # return fetch_helper({'company': company})
        return res

def delete_helper(req, options):
    try:
        booking_id = req['booking_id']
        company = req['company']
        item = { 'booking_id': booking_id}
        res = table.delete_item(
            Key = item
        )
        # return_all = fetch_helper()
    except Exception as e:
        print(f"Error is from delete_helper: {e}")
        res = 'Error'
    finally:
        if options in globals():
            return options.callback(options.payload)
        # return fetch_helper({'company': company})
        return res

# iterates over payload and rejects booking if any cells are not free
# TODO convert get_item check to transaction
def add_booking(event, context):
    status =  400
    res = 'add booking'
    add_booking_res = None
    try:
        print(json.dumps(event['body']))
        booking_params = json.loads(event['body'])

        booking_id = booking_params['booking_id']
 
        company = booking_params['company']
    
        check = table.get_item(
            Key = {
                "booking_id" : booking_id,
                "company" : company
            }
        )
        print(check)
        if 'Item' in check:
            status = 403
            add_booking_res = 'booking already exists!'
            print(add_booking_res)
            # add_booking_res = fetch_helper({ "company" : company})
        # just concactenate the company and datalookups to create unique bookingid
        # bookings expire after day is complete
        elif 'Item' not in check:
            reqPayload = {
                "booking_id" : booking_id,
                "company" : company,
                "booking_name" : booking_params['booking_name'],
                "room_id" : booking_params['room_id'],
                "organizer_id" : booking_params['organizer_id'],
                "start_time" : booking_params['start_time'],
                "end_time" : booking_params['end_time']
            }
            res = add_helper(json.dumps(reqPayload))
            add_booking_res = res
            status = 200
            if add_booking_res == 'Error':
                status = 401
    except Exception as e:
        print(f"Error is from add_booking: {e}")
    finally:
        return {
            'statusCode': status,
            'headers': headers,
            'body' : add_booking_res
        }
    
def get_booking(event,context):
    #  needs at least company
    # fetches one or all based on presence of booking_id
    status = 400
    res = "get booking"
    get_booking_res = None
    try:
        booking_params = event['queryStringParameters']
        res = fetch_helper(booking_params)
        print(res)
        # get_booking_res = json.dumps(res)
        get_booking_res = res
        status = 200
    except Exception as e:
        get_bookings_res = "Error"
        print(f"Error is from get_booking: {e}")
        status = 403
    finally:
        return {
            'statusCode': status,
            'headers': headers,
            # 'body': get_booking_res
            'body': str(json.dumps(get_booking_res))
        }

def update_booking(event,context):
    status = 400
    res = "updating booking"
    update_booking_res = None
    try:
        # TODO: will need to be in body like post is due to crazy long strings
        booking_params = event['queryStringParameters']
        reqPayload = {
            "booking_id" : booking_params['booking_id'],
            "booking_name" : booking_params['booking_name'],
            "company" : booking_params['company'],
            "room_id" : booking_params['room_id'],
            "organizer_id" : booking_params['organizer_id'],
            "start_time" : booking_params['start_time'],
            "end_time" : booking_params['end_time']
        }
        res = delete_helper({'booking_id': booking_params['old_booking_id']}, {payload: reqPayload, callback: add_helper})
        update_booking_res = res
        status = 200
        if res == 'Error':
            status = 403
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
    delete_booking_res = None
    try:
        booking_path_params = event['pathParameters']
        booking_query_params = event['queryStringParameters']
        print(params)
        booking_id = booking_path_params['booking_id']
        company = booking_query_params['company']
        req = { 'booking_id': booking_id, 'company': company}
        res = delete_helper(req)
        delete_booking_res = res
        status = 200
        if delete_booking_res == 'Error':
            status = 403
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
        
