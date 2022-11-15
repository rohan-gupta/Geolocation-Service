"""Module for job functions."""
try:
    import unzip_requirements
except ImportError:
    pass
import ujson
from coverer.coverage import cover_territory


def get_all_latitude_longitude(event, _context):
    """Job handler for coverer."""
    try:
        body = ujson.loads(event["body"]) if "body" in event else {}
        territory, country_code = None, None
        if "territory" in body:
            territory = body["territory"]
        elif "countryCode" in body:
            country_code = body["countryCode"]
        latitude_longitude = cover_territory(country_code=country_code, territory=territory)
        status_code = 200
    except RuntimeError:
        status_code = 200
    response = {
        "statusCode": status_code,
        "headers": {
            "content-type": "application/json"
        },
        "body": ujson.dumps(latitude_longitude),
        "isBase64Encoded": False,
    }
    return response
