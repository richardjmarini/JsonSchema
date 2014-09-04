# /validate
=========

is a simple RESTful service that validates JSON objects against a JSON schema. 

Validating a JSON object:
```
URI: validate/<schema_name>/
Method: POST 
Request Headers:
	Accept: application/json
Request Data:
	Content-Type: application/json
```

```
example using 'address' schema:
{
   "address1": "17 Battery Pl",
   "city": "New York",
   "state": "NY",
   "zipcode":  "10017",
   "country": "USA",
   "geolocation": {
      "longitude": 0
      "latitude": 0
   }
}
```
```	
Response Headers: 
	Content-Type: application/json
Response Data: 
```

```
example using 'address' schema:
{
    "$schema": "http://json-schema.org/draft-04/schema#",
    "title": "address",
    "description": "address",
    "type": "object",
    "properties": {
        "address1": {"$ref": "/schema/addressline"},
        "address2": {"$ref": "/schema/addressline"},
        "city": {"$ref": "/schema/city"},
        "state": {"$ref": "/schema/state"},
        "zipcode": {"$ref": "/schema/zipcode"},
        "country": {"$ref": "/schema/country"},
        "geolocation": {"$ref": "/schema/geolocation"},
        "neighborhood": {"$ref": "/schema/name"},
        "cross_street": {"$ref": "/schema/addressline"},
        "directions": {"$ref": "/schema/directions"}
    },
    "required": ["address1", "city", "state", "zipcode"]
}
```

Status Codes:
```
200: schema validated successfully
400: Bad Request (schema failed validation)
401: Unauthorized
404: Schema not found
417: Expectation Not Met (eg, JSON Schema definition is invalid)
```

