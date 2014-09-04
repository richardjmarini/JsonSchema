# /transform
=========

is a simple RESTful service that transforms one JSON object (ie, the standard message/event. document from the data marhsalling system) into another (ie, v3, v2, or some other publisher message document).

transforming JSON object:
```
URI: transform/<schema_name_to_transform_to>/
Method: POST 
Request Headers:
	Accept: application/json
Request Data:
	Content-Type: application/json
```

```
{
    "$schema": "http://json-schema.org/draft-04/schema/",
    "title": "event",
    "description": "The standard message event for Data Marshalling System",
    "type": "object",
    "properties": {
        "schema_url": { "$ref": "/schema/url" },
        "event_id": { "$ref": "/schema/uuid" },
        "timestamp": { "$ref": "/schema/timestamp" },
        "action": {"$ref": "/schema/event/action" },
        "payload_type": { "$ref": "/schema/event/payloadtype" },
        "payload": {
 		... document definition ...
	}
    },
    "required": ["schema_url", "event_id", "timestamp", "payload_type", "payload"]
}
```
	
```
Response Headers: 
  Content-Type: application/json
Response Data: 
```

```
{... transformed document defintion ...}
```

Status Codes:

```
200: Object transformed successfully
400: Bad Request (could not transform object)
401: Unauthorized
404: Schema not found. 
417: Expectation Not Met (eg, JSON Schema definition is invalid)
```

