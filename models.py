"""Represent models for near-Earth objects and their close approaches.

The `NearEarthObject` class represents a near-Earth object. Each has a unique
primary designation, an optional unique name, an optional diameter, and a flag
for whether the object is potentially hazardous.

The `CloseApproach` class represents a close approach to Earth by an NEO. Each
has an approach datetime, a nominal approach distance, and a relative approach
velocity.

A `NearEarthObject` maintains a collection of its close approaches, and a
`CloseApproach` maintains a reference to its NEO.

The functions that construct these objects use information extracted from the
data files from NASA, so these objects should be able to handle all of the
quirks of the data set, such as missing names and unknown diameters.

You'll edit this file in Task 1.
"""
import math

from helpers import cd_to_datetime, datetime_to_str


class NearEarthObject:
    """A near-Earth object (NEO).

    An NEO encapsulates semantic and physical parameters
    about the object, such as its primary designation (required, unique), IAU
    name (optional), diameter in kilometers (optional - sometimes unknown),
    and whether it's marked as potentially hazardous to Earth.

    A `NearEarthObject` also maintains a collection of its close approaches -
    initialized to an empty collection, but eventually populated in the
    `NEODatabase` constructor.
    """
    def __init__(self, **info):
        """Create a new `NearEarthObject`.

        :param info: A dictionary of excess keyword arguments
                     supplied to the constructor.
        """
        self.designation = info.get('designation', None)
        self.name = None if len(info['name']) == 0 else info.get('name')
        self.diameter = float('nan') if len(info['diameter']) == 0 \
            else float(info['diameter'])
        self.hazardous = True if info['hazardous'].upper() == 'Y' else False

        # Create an empty initial collection of linked approaches.
        self.approaches = []

    @property
    def fullname(self):
        """ Return a representation of the full name of this NEO."""
        dangerous = 'is definitely' if self.hazardous else 'is not potentially'
        return (f'{self.designation} {self.name} has a diameter of '
                f'{self.diameter} km and {dangerous} hazardous')

    def __str__(self):
        """Return `str(self)`."""
        return f"A NearEarthObject {self.fullname}"

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string
           representation of this object.
        """
        return (f"NearEarthObject(designation={self.designation!r},"
                f" name={self.name!r}, "
                f"diameter={self.diameter:.3f}, "
                f" hazardous={self.hazardous!r}")

    def serialize(self):
        neo_parse_dict = {
            "designation": self.designation,
            "name": '' if self.name is None else self.name,
            "diameter_km": self.diameter,
            "potentially_hazardous": self.hazardous
        }

        return neo_parse_dict


class CloseApproach:
    """A close approach to Earth by an NEO.

    A `CloseApproach` encapsulates information about the NEO's
    close approach to Earth, such as the date and time (in UTC) of
    closest approach, the nominal approach distance in astronomical
    units, and the relative approach velocity in kilometers per second.

    A `CloseApproach` also maintains a reference to its `NearEarthObject` -
    initially, this information (the NEO's primary designation) is saved in a
    private attribute, but the referenced NEO is eventually replaced in the
    `NEODatabase` constructor.
    """
    def __init__(self, **info):
        """Create a new `CloseApproach`.

        :param info: A dictionary of excess keyword arguments
                     supplied to the constructor.
        """
        self._designation = info.get('designation', None)

        self.time = cd_to_datetime(info.get('time'))
        self.distance = info.get('distance', float('nan'))
        self.velocity = info.get('velocity', float('nan'))
        # self.neo_name = NearEarthObject().fullname
        # Create an attribute for the referenced NEO, originally None.
        self.neo = None

    @property
    def time_str(self):
        """
        Return a formatted representation of this
        CloseApproach`'s approach time.

        The value in `self.time` should be a Python `datetime` object. While a
         datetime` object has a string representation,
        the default representation
        includes seconds - significant figures that don't exist in our input
        data set.

        The `datetime_to_str` method converts a `datetime` object to a
        formatted string that can be used in human-readable representations and
        in serialization to CSV and JSON files.

        build a formatted representation of the approach time.
        """
        return f'{datetime_to_str(self.time)}'

    def __str__(self):
        """ Return `str(self)`.
           a human-readable string representation.)
        """
        return f"{self.__repr__()}"

    def __repr__(self):
        """ Return `repr(self)`, a computer-readable string
            representation of this object.
        """
        return f"A Close Approach(time={self.time_str!r}, " \
               f"distance={self.distance:.2f}, " \
               f"velocity={self.velocity:.2f}, " \
               f"neo={self.neo!r}, _designation={self._designation!r})"

    def serialize(self):
        clean_dict = {
            "datetime_utc": datetime_to_str(self.time),
            "distance_au": self.distance,
            "velocity_km_s": self.velocity,
            'designation': self.neo.designation,
            'name': '' if self.neo.name is None else self.neo.name,
            'diameter_km': self.neo.diameter,
            'potentially_hazardous': self.neo.hazardous
        }

        return clean_dict
