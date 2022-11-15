"""Module for coverage functions."""
from coverer.logic import get_latitude_longitude


def cover_territory(country_code, territory):
    """Returns latitude longitude list for a given country code."""
    latitude_longitude = {
        "latitudeLongitude": get_latitude_longitude(country_code=country_code, territory=territory)
    }
    return latitude_longitude
