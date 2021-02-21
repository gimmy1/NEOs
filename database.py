"""A database encapsulating collections of near-Earth objects and their close approaches.

A `NEODatabase` holds an interconnected data set of NEOs and close approaches.
It provides methods to fetch an NEO by primary designation or by name, as well
as a method to query the set of close approaches that match a collection of
user-specified criteria.

Under normal circumstances, the main module creates one NEODatabase from the
data on NEOs and close approaches extracted by `extract.load_neos` and
`extract.load_approaches`.
"""
from collections import defaultdict
from models import NearEarthObject, CloseApproach

class NEODatabase:
    """A database of near-Earth objects and their close approaches.

    A `NEODatabase` contains a collection of NEOs and a collection of close
    approaches. It additionally maintains a few auxiliary data structures to
    help fetch NEOs by primary designation or by name and to help speed up
    querying for close approaches that match criteria.
    """
    def __init__(self, neos, approaches):
        """
        :param neos: A collection of `NearEarthObject`s.
        :param approaches: A collection of `CloseApproach`es.
        """
        self._neos = neos
        self._approaches = approaches

        self.neos_designation = defaultdict(NearEarthObject)
        self.neos_name = defaultdict(NearEarthObject)

        for neo in self._neos:
            self.neos_designation[neo.designation] = neo
            self.neos_name[neo.name] = neo
        
        for ca in self._approaches:
            if ca._designation in self.neos_designation:
                self.neos_designation[ca._designation].approaches.append(ca)
                ca.neo = self.neos_designation[ca._designation]


    def get_neo_by_designation(self, designation):
        """
        :param designation: The primary designation of the NEO to search for.
        :return: The `NearEarthObject` with the desired primary designation, or `None`.
        """
        return self.neos_designation.get(designation, None)

    def get_neo_by_name(self, name):
        """
        :param name: The name, as a string, of the NEO to search for.
        :return: The `NearEarthObject` with the desired name, or `None`.
        """
        # : Fetch an NEO by its name.
        return self.neos_name.get(name, None)

    def query(self, filters=()):
        """
        :param filters: A collection of filters capturing user-specified criteria.
        :return: A stream of matching `CloseApproach` objects.
        """
        for approach in self._approaches:
            flags = list(map((lambda x: x(approach)), filters))
            if all(flags):
                yield approach
