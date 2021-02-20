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
            diameter = to_float(elem.get("diameter",
                                float("nan")))
            hazardous = to_boolean(elem.get("pha", "N"))
            result.add(NearEarthObject(
                designation,
                name,
                diameter,
                hazardous
            ))
    return result


def load_approaches(cad_json_path):
    """Read close approach data from a JSON file.

    :param neo_csv_path: A path to a JSON file containing data about close approaches.
    :return: A collection of `CloseApproach`es.
    """
    result = set()
    with open(cad_json_path, "r") as infile:
        contents = json.load(infile).get("data", None)
        if contents:
            for elem in contents:
                designation = elem[0]
                time = elem[3]
                distance = to_float(elem[4])
                velocity = to_float(elem[7])
                result.add(CloseApproach(designation,
                                         time,
                                         distance,
                                         velocity))
    return result
