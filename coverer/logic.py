"""Module for logic functions."""
import os
import boto3
import ujson
from s2geometry import S2LatLng, S2RegionCoverer, S2Loop
from fastkml import kml


def read_file_from_s3(bucket, filepath):
    """Returns python style dictionary of the json file read."""
    s3_client = boto3.resource("s3")
    try:
        s3_object = s3_client.Object(f"fp-apac-vci-gaia-rover-condition-{bucket}", filepath)
        filedata = ujson.load(s3_object.get()["Body"])
    except Exception:
        filedata = None
    return filedata


def get_territory(country_code, territory):
    """Returns territory boundary for a country code."""
    if not territory and country_code:
        territory = read_file_from_s3(os.getenv("STAGE"), f"territories/{country_code}.json")["sg"]
    elif not territory and not country_code:
        territory = []
    for index, coordinate in enumerate(territory):
        territory[index] = list(map(float, coordinate.split(",")))
    return territory


def get_s2_point_from_latitude_longitude(latitude, longitude):
    """Returns S2 point for a given latitude longitude."""
    return S2LatLng.FromDegrees(latitude, longitude).ToPoint()


def get_latitude_longitude(country_code=None, territory=None,
                           min_level=13, max_level=13, max_cells=500):
    """Returns a list of latitude and longitude for a given country code."""
    territory = get_territory(country_code=country_code, territory=territory)
    if territory:
        s2_points = []
        for coordinate in territory:
            s2_points.append(get_s2_point_from_latitude_longitude(coordinate[0], coordinate[1]))
        s2_loop = S2Loop()
        s2_loop.Init(s2_points)
        s2_region = S2RegionCoverer()
        s2_region.set_min_level(min_level)
        s2_region.set_max_level(max_level)
        s2_region.set_max_cells(max_cells)
        s2_covering = s2_region.GetCovering(s2_loop)
        latitude_longitude = []
        latitude_longitude = [s2_cell.ToLatLng().ToStringInDegrees() for s2_cell in s2_covering]
    else:
        latitude_longitude = None
    return latitude_longitude


def get_latitude_longitude_from_kml_file(filepath):
    """Reads kml files and converts them to a latlng list."""
    with open(filepath) as myfile:
        doc = myfile.read()
    k = kml.KML()
    k.from_string(doc.encode('utf-8'))
    outer_feature = list(k.features())
    inner_feature = list(outer_feature[0].features())
    # Generates boundary latlong from file
    latitude_longitude_list = []
    for point in inner_feature:
        point_list = list(point.geometry.exterior.coords)
        for solo_pt in point_list:
            if float(solo_pt[0]) < float(solo_pt[1]):
                latitude_longitude_list.append(f"{solo_pt[0]}, {solo_pt[1]}")
            else:
                latitude_longitude_list.append(f"{solo_pt[1]}, {solo_pt[0]}")
    # Generates result using core feature of repo
    latitude_longitude = get_latitude_longitude(territory=latitude_longitude_list)
    return latitude_longitude
