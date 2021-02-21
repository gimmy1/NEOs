"""Extract data on near-Earth objects and close approaches from CSV and JSON files.

The `load_neos` function extracts NEO data from a CSV file, formatted as
described in the project instructions, into a collection of `NearEarthObject`s.

The `load_approaches` function extracts close approach data from a JSON file,
formatted as described in the project instructions, into a collection of
`CloseApproach` objects.

The main module calls these functions with the arguments provided at the command
line, and uses the resulting collections to build an `NEODatabase`.

"""
import csv
import json

from helpers import to_boolean, to_float
from models import NearEarthObject, CloseApproach


def load_neos(neo_csv_path):
    """Read near-Earth object information from a CSV file.

    :param neo_csv_path: A path to a CSV file containing data about near-Earth objects.
    :return: A collection of `NearEarthObject`s.
    """
    result = set()
    with open(neo_csv_path, "r") as infile:
        reader = csv.DictReader(infile)
        for elem in reader:
            designation = elem.get("pdes", None)
            name = elem.get("name", None)
            diameter = elem.get("diameter")
            hazardous = elem.get("pha")
            result.add(NearEarthObject(
                designation=designation,
                name=name,
                diameter=diameter,
                hazardous=hazardous
            ))
    return result


def load_approaches(cad_json_path):
    """Read close approach data from a JSON file.

    :param neo_csv_path: A path to a JSON file containing data about close approaches.
    :return: A collection of `CloseApproach`es.
    """
    result = set()
    with open(cad_json_path, "r") as infile:
        contents = json.load(infile)
        
        for elem in contents['data']:
            result.add(CloseApproach(designation=elem[0],
                                     time=elem[3],
                                     distance=elem[4],
                                     velocity=elem[7]))    
    
    return result
