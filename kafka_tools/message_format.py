import jsonschema


SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Message payload",
    "type": "object",
    "properties": {
        "id": {
            "type": "object"
        },
        "action": {
            "type": "string",
            "pattern": "(create|update|delete)"
        },
        "type": {
            "type": "string"
        },
        "title": {
            "type": "string"
        },
        "timestamp": {
            "type": "string",
            "format": "date-time"
        },
        "source": {
            "type": "string"
        },
        "version": {
            "anyOf": [
                {"type": "null"},
                {"type": "integer"}
            ]
        }
    },
    "additionalProperties": False,
    "required": ["id", "action", "type", "title", "timestamp", "source", "version"]
}


def validate_payload(payload):
    return jsonschema.validate(payload, SCHEMA, format_checker=jsonschema.FormatChecker())
