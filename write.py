"""
This module exports two functions: `write_to_csv` and `write_to_json`, each of
which accept an `results` stream of close approaches and a path to which to
write the data.

These functions are invoked by the main module with the output of the `limit`
function and the filename supplied by the user at the command line. The file's
extension determines which of these functions is used.
"""
import csv
import json

from helpers import datetime_to_str


def write_to_csv(results, filename):
    """
    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the data should be saved.
    """
    fieldnames = (
        "datetime_utc",
        "distance_au",
        "velocity_km_s",
        "designation",
        "name",
        "diameter_km",
        "potentially_hazardous",
    )
    with open(filename, "w") as outfile:
        writer = csv.writer(outfile)
        writer.writerow(fieldnames)
        for result in results:
            ca = result.serialize()
            writer.writerow(
                [
                    ca["datetime_utc"],
                    ca["distance_au"],
                    ca["velocity_km_s"],
                    ca["neo"]["designation"],
                    ca["neo"]["name"],
                    ca["neo"]["diameter_km"],
                    ca["neo"]["potentially_hazardous"],
                ]
            )


def write_to_json(results, filename):
    """
    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like o
    bject pointing to where the data should be saved.
    """
    output = [result.serialize() for result in results]

    with open(filename, "w") as outfile:
        json.dump(output, outfile, indent=2)
