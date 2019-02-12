"""Module handles Chalice functionality"""
import io
import random
from datetime import datetime

import boto3
import requests
from chalice import Chalice, Response

app = Chalice(app_name='advanced-local')
app.debug = True

S3 = boto3.client('s3')
BUCKET = 'advanced-local'
POKEMON_COUNT = 807


@app.route('/')
def index():
    return "Welcome to my API! Please refer to the README further help!"

@app.route('/status')
def status():
    """Returns the status of the API route

    Note: This is for Challenge 1: API status.

    Returns:
        dict: Data containg information about the server
    """

    resp = {
        'status': 'OK',
        'date': str(datetime.now())
    }

    return Response(
        headers={'Content-Type': 'application/json'},
        body=resp,
        status_code=200
    )

@app.route('/pokemon')
def pokemon():
    """Fetches a number of pokemon and compare some of
    their attributes against each other

    Note: This is for Challenge 2:
    Transform publicly available data into something fun.

    Returns:
        Response: Chalice response object
    """
    query_params = app.current_request.query_params
    if query_params and 'count' in query_params:
        count = int(query_params['count'])
    else:
        count = 2

    p_list = []
    for _ in range(count):
        result = requests.get(
            "https://pokeapi.co/api/v2/pokemon/{id}".format(
                id=random.randint(1,POKEMON_COUNT)
            )
        )
        p_list.append(result.json())

    body = {
        'pokemon': [p['name'] for p in p_list],
        'comparison': {}
    }

    for attr in ['height', 'weight']:
        attrs = [p[attr] for p in p_list]
        body['comparison']['max_'+attr] = p_list[attrs.index(max(attrs))]['name']
        body['comparison']['min_'+attr] = p_list[attrs.index(min(attrs))]['name']

    return Response(
        headers={'Content-Type': 'application/json'},
        body=body
    )

@app.route("/upload", methods=['POST'],
           content_types=['application/octet-stream'])
def upload_image():
    """Uploads a file to S3.

    Note: This is for Challenge 3: Upload a PNG image to S3.

    URI Query Params:
        file_name(optional): File name for upload
    Returns:
        Response: Chalice response object
    """
    response = Response(
        headers={'Content-Type': 'application/json'},
        body=None
    )

    # Check to make sure that there is an upload with content
    if not app.current_request.raw_body:
        response.body={"message": 'No file contents were found!'}
        response.status_code=400
        return response

    # Optional paramter to change file name
    query_params = app.current_request.query_params
    if query_params and 'file_name' in query_params:
        file_name = app.current_request.query_params['file_name']
    else:
        file_name = 'file_{date}.png'.format(
            date=datetime.now().strftime("%Y%m%d%H%M%S")
        )

    # Current file to byte object
    request_image = io.BytesIO()
    request_image.write(app.current_request.raw_body)
    request_image.seek(0)

    # Uploads byte object to specificed S3 Bucket
    try:
        location = S3.get_bucket_location(Bucket=BUCKET)
        S3.upload_fileobj(
            request_image, BUCKET, file_name,
            ExtraArgs={"ContentType": "image/png"}
        )
        response.body = {
            'message': 'success',
            'filename': file_name,
            'url': "https://s3-{location}.amazonaws.com/{bucket}/{file}".format(
                location=location['LocationConstraint'],
                bucket=BUCKET,
                file=file_name
            )
        }
        response.status_code = 200
    except Exception:
        response.body = {
            'message': 'Failed to upload file'
        }
        response.status_code = 400

    return response
