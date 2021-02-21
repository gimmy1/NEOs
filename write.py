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
    fieldnames = ("datetime_utc", "distance_au", "velocity_km_s", "designation", "name", "diameter_km", "potentially_hazardous")
    with open(filename, "w") as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        for result in results:
            ca = result.serialize()
            neo = result.neo.serialize()
            writer.writerow(
                [
                    ca["datetime_utc"],
                    ca["distance_au"],
                    ca["velocity_km_s"],
                    ca["designation"],
                    neo["name"],
                    neo["diameter_km"],
                    neo["potentially_hazardous"]
                ]
            )



def write_to_json(results, filename):
    """
    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the data should be saved.
    """
    with open(filename, "w") as outfile:
        out = []
        for result in results:
            ca = result.serialize()
            neo = result.neo.serialize()
            out.add(**ca, **{"neo": neo})
        outfile.write(out, indent=2)
        


