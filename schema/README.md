# /schema
=========

is a simple RESTful service that serves out JSON Schema definitions that can be used to dynamically build objects and/or used by the the /validate service to validate those objects.

Fetching a Schema:

```
URI: schema/<name>/
Method: GET 
Request Headers:
        Accept: application/json
Request Data: N/A
Response Headers: 
        Content-Type: application/json
Response Data: (example based on /schema/phone)
```
```
{
    "$schema": "http://json-schema.org/draft-04/schema#",
    "title": "phone",
    "description": "Phone",
    "type": "string",
    "pattern": "^(\\([0-9]{3}\\))?[0-9]{3}-[0-9]{4}$"
}
```

Response Status Codes:
```
200: Schema returned successfully 
400: Bad Request
401: Unauthorized
404: Schema not found. 
417: Expectation Not Met (eg, JSON Schema definition is invalid)
```

