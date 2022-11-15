"""Module for unit tests for logic.py."""
import re
import ujson
import pytest
import s2geometry
from coverer import logic


@pytest.fixture
def _mock_env(monkeypatch):
    """Mock the runtime environment."""
    monkeypatch.setenv("STAGE", "dev")
    monkeypatch.setattr(logic, "read_file_from_s3", mock_read_file_from_s3)


def mock_read_file_from_s3(*_args, **_kwargs):
    """Mocks the output of read file from s3 function."""
    return ujson.load(open("tests/test_data/territory_data.json", "r"))


def test_get_coordinates(_mock_env):
    """Unit test for get_coordinates."""
    coordinates = logic.get_territory("sg", None)
    assert isinstance(coordinates, list)
    assert isinstance(coordinates[0], list)


def test_get_s2_point_from_latitude_longitude(_mock_env):
    """Unit test for get_s2_point_from_latitude_longitude."""
    s2point = logic.get_s2_point_from_latitude_longitude(1.301255, 103.712055)
    assert isinstance(s2point, s2geometry.S2Point)


def test_get_latitude_longitude(_mock_env):
    """Unit test for get_latitude_longitude_for_country_code."""
    mock_territory = [
        "1.301255, 103.712055",
        "1.284628, 103.777786",
        "1.264043, 103.830055",
        "1.290962, 103.875987",
        "1.389137, 103.993195",
        "1.393095, 103.936175",
        "1.462765, 103.837182",
        "1.446931, 103.770659",
        "1.404179, 103.664538",
        "1.339258, 103.634444"
    ]
    latitude_longitude_1 = logic.get_latitude_longitude(country_code="sg")
    latitude_longitude_2 = logic.get_latitude_longitude(territory=mock_territory)
    assert isinstance(latitude_longitude_1, list)
    assert re.match(r"[\d\.\,]*", latitude_longitude_1[0])
    assert isinstance(latitude_longitude_2, list)
    assert re.match(r"[\d\.\,]*", latitude_longitude_2[0])
    assert latitude_longitude_1 == latitude_longitude_2

def test_get_latitude_longitude_from_kml_file():
    """Unit test for kml_file_reader."""
    filepath = './tests/test_data/test_fukuoka.kml'
    results = logic.get_latitude_longitude_from_kml_file(filepath)
    assert results[0] == "33.618397,130.405780"
