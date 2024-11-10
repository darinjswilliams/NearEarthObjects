"""A database encapsulating collections of near-Earth objects and their
close approaches.

A `NEODatabase` holds an interconnected data set of NEOs and close approaches.
It provides methods to fetch an NEO by primary designation or by name, as well
as a method to query the set of close approaches that match a collection of
user-specified criteria.

Under normal circumstances, the main module creates one NEODatabase from the
data on NEOs and close approaches extracted by `extract.load_neos` and
`extract.load_approaches`.

You'll edit this file in Tasks 2 and 3.
"""
import functools


def memoize(func):
    cache = {}
    @functools.wraps(func)
    def memoized_func(*args, **kwargs):
        key = (args, tuple(kwargs.items()))
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        return cache[key]

    return memoized_func

class NEODatabase:
    """A database of near-Earth objects and their close approaches.

    A `NEODatabase` contains a collection of NEOs and a collection of close
    approaches. It additionally maintains a few auxiliary data structures to
    help fetch NEOs by primary designation or by name and to help speed up
    querying for close approaches that match criteria.
    """

    def __init__(self, neos, approaches):
        """Create a new `NEODatabase`.

        As a precondition, this constructor assumes that the collections of
        NEOs and close approaches haven't yet been linked - that is, the
        `.approaches` attribute of each `NearEarthObject` resolves to an empty
        collection, and the `.neo` attribute of each `CloseApproach` is None.

        However, each `CloseApproach` has an attribute (`._designation`) that
        matches the `.designation` attribute of the corresponding NEO. This
        constructor modifies the supplied NEOs and close approaches to
        link them together - after it's done, the `.approaches`
        attribute of each NEO has a collection of that NEO's close approaches,
        and the `.neo` attribute of each close approach references the
        appropriate NEO.

        :param neos: A collection of `NearEarthObject`s.
        :param approaches: A collection of `CloseApproach`es.
        """
        self._neos = neos
        self._approaches = approaches

        self.neo_lookup_designation = {
            neo.designation: neo for neo in self._neos}
        self.neo_lookup_name = {neo.name: neo for neo in self._neos}


        # for approach in self._approaches:
        #     neo = self.neo_lookup_designation.get(approach._designation)
        #     approach.neo = neo
        #     neo.approaches.append(approach)

    @memoize
    def get_neo_by_designation(self, designation):
        return self.neo_lookup_designation.get(designation)


    @memoize
    def get_neo_by_name(self, name):
        return self.neo_lookup_name.get(name)


    def query(self, filters=()):
        for approach in self._approaches:
            if all(filter(approach) for filter in filters):
                yield approach

    def _link_approaches_to_neos(self, close_approaches):
        neo_objects = self.get_neo_by_designation(close_approaches._designation)
        close_approaches.neo = neo_objects
        neo_objects.approaches.append(close_approaches)

    def link_all_approaches(self):
        for coa_approach in self._approaches:
            self._link_approaches_to_neos(coa_approach)


    # def get_neo_by_designation(self, designation):
    #     """Find and return an NEO by its primary designation.
    #
    #     If no match is found, return `None` instead.
    #
    #     Each NEO in the data set has a unique primary designation, as a string.
    #
    #     The matching is exact - check for spelling and capitalization if no
    #     match is found.
    #
    #     :param designation: The primary designation of the NEO to search for.
    #     :return: The `NearEarthObject` with the desired primary designation,
    #     or `None`.
    #     """
    #     return self.neo_lookup_designation.get(designation)

    # def get_neo_by_name(self, name):
    #     """Find and return an NEO by its name.
    #
    #     If no match is found, return `None` instead.
    #
    #     Not every NEO in the data set has a name. No NEOs are associated with
    #     the empty string nor with the `None` singleton.
    #
    #     The matching is exact - check for spelling and capitalization if no
    #     match is found.
    #
    #     :param name: The name, as a string, of the NEO to search for.
    #     :return: The `NearEarthObject` with the desired name, or `None`.
    #     """
    #     return self.neo_lookup_name.get(name)

    # def query(self, filters=()):
    #     """Query close approaches to generate those that match a
    #     collection of filters.
    #
    #     This generates a stream of `CloseApproach` objects that match all
    #     of the provided filters.
    #
    #     If no arguments are provided, generate all known close approaches.
    #
    #     The `CloseApproach` objects are generated in internal order,
    #     which isn't guaranteed to be sorted meaningfully, although is
    #     often sorted by time.
    #
    #     :param filters: A collection of filters capturing user-specified
    #      criteria.
    #     :return: A stream of matching `CloseApproach` objects.
    #     """
    #
    #     for approach in self._approaches:
    #         if all(filter(approach) for filter in filters):
    #             yield approach
