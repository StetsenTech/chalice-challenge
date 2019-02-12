# Chalice Challenge Application

This repository is dedicated to a code challenge using the AWS Chalice framework.

## Documentation

- [Getting Started](GETTING_STARTED.md) - Step by step for starting on project

## Usage

### Starting Chalice Challenge Application

When using chalice with this project, please use the `chalice-challenge` folder when running commands.
After cloning this repository, use the following command to change directory to this project.

```
cd chalice-challenge
```

#### AWS Server

Chalice requires AWS credentials to be properly set up on server's environment. For setup, please visit the [Chalice GitHub repository](https://github.com/awslabs/chalice#credentials).

```
$ chalice deploy
Creating deployment package.
Updating policy for IAM role: advanced-local-dev
Updating lambda function: advanced-local-dev
Updating rest API
Resources deployed:
  - Lambda ARN: arn:aws:lambda:us-east-2:868951015787:function:advanced-local-dev
  - Rest API URL: https://ukpwegu49a.execute-api.us-east-2.amazonaws.com/api/
```

#### Local Server

Chalice can deployed locally if server access isn't available.

```
$ chalice local
Found credentials in shared credentials file: ~/.aws/credentials
Serving on http://127.0.0.1:8000
```

### Challenge 1

This challenge allows you to see the status of the chalice API.

#### Status

To get the status of the API, use the `/status` route.

```bash
$ curl -X GET https://ukpwegu49a.execute-api.us-east-2.amazonaws.com/api/status
```
```json
{
  "status": "OK",
  "date": "2019-02-12 02:45:48.011744"
}
```

### Challenge 2

This challenge uses the Public API "PokéAPI" to retrieve information different Pokemon and compare different aspects
of them such height and weight.

#### Compare Two Pokemon

```
$ curl -X GET https://ukpwegu49a.execute-api.us-east-2.amazonaws.com/api/pokemon
```
```json
{
  "comparison": {
    "min_height": "wartortle",
    "min_weight": "wartortle",
    "max_height": "barbaracle",
    "max_weight": "barbaracle"
  },
  "pokemon": ["barbaracle", "wartortle"]
}
```

### Compare Ten Pokemon

```
$ curl -X GET https://ukpwegu49a.execute-api.us-east-2.amazonaws.com/api/pokemon?count=10
```
```json
{
  "comparison": {
    "min_height": "cutiefly",
    "min_weight": "cutiefly",
    "max_height": "darmanitan-standard",
    "max_weight": "munchlax"
  },
  "pokemon": [
    "electrode",
    "unown",
    "munchlax",
    "cutiefly",
    "golett",
    "slurpuff",
    "darmanitan-standard",
    "elgyem",
    "pineco",
    "ledyba"
  ]
}
```

### Challenge 3

This challenge uploads a PNG image to AWS S3 Bucket.

#### Upload PNG Image to S3
```
$ curl -X POST https://ukpwegu49a.execute-api.us-east-2.amazonaws.com/api/upload --upload-file upload_image.png --header "Content-Type:application/octet-stream"
```
```json
{
    "url": "https://s3-us-east-2.amazonaws.com/advanced-local/file_20190212031902.png",
    "message": "success",
    "filename": "file_20190212031902.png"
}
```

#### Upload PNG Image to S3 with Specificed Name
```
$ curl -X POST https://ukpwegu49a.execute-api.us-east-2.amazonaws.com/api/upload?file_name=special.png --upload-file upload_image.png --header "Content-Type:application/octet-stream"
```
```json
{
    "url": "https://s3-us-east-2.amazonaws.com/advanced-local/special.png",
    "message": "success",
    "filename": "special.png"
}
```
