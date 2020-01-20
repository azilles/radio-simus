import astropy.units as u
from typing import Optional


class AlreadySet(Exception):
    """Raised when attempting to re-set an already set attribute"""
    pass


class CheckedShower():
    """An example of a mutable container with both static and runtime checks

    1. A static analyses can be done with mypy. It will ensure that the proper
       types are used as arguments when setting the shower attributes.

    2. In addition using the @property class decorator we can perform runtime
       checks when an instance attribute is modified.
    """

    _attributes = ["showerID", "primary", "energy", "zenith", "azimuth"]


    def __init__(self, **kwargs):
        self.__showerID: Optional[str] = None
        self.__primary: Optional[str] = None
        self.__energy: Optional[u.Quantity] = None
        self.__zenith: Optional[u.Quantity] = None
        self.__azimuth: Optional[u.Quantity] = None

        for attr, value in kwargs.items():
            if attr not in self._attributes:
                raise ValueError(f"Invalid attribute {attr}")
            setattr(self, attr, value)


    def __str__(self) -> str:
        attributes = ", ".join([attr + "=" + repr(getattr(self, attr))
                                for attr in self._attributes])
        return f"{self.__class__.__name__}({attributes})"


    @staticmethod
    def _assert_not_set(attr):
        if attr is not None:
            raise AlreadySet()


    @property
    def showerID(self) -> str:
        """The very unique ID of a shower"""
        return self.__showerID

    @showerID.setter
    def showerID(self, value: str):
        self._assert_not_set(self.__showerID)
        self.__showerID = value


    @property
    def primary(self) -> str:
        """The primary particle initiating the shower"""
        return self.__primary

    @primary.setter
    def primary(self, value: str):
        self._assert_not_set(self.__primary)
        self.__primary = value


    @property
    def energy(self) -> u.Quantity:
        """The total energy contained in the shower"""
        return self.__energy

    @energy.setter
    def energy(self, value: u.Quantity):
        self._assert_not_set(self.__energy)
        self.__energy = value.to(u.eV)


    @property
    def zenith(self) -> u.Quantity:
        """The zenith angle of the shower axis"""
        return self.__zenith

    @zenith.setter
    def zenith(self, value: u.Quantity):
        self._assert_not_set(self.__zenith)
        self.__zenith = value.to(u.deg)


    @property
    def azimuth(self) -> u.Quantity:
        """The azimuth angle of the shower axis"""
        return self.__azimuth

    @azimuth.setter
    def azimuth(self, value: u.Quantity):
        self._assert_not_set(self.__azimuth)
        self.__azimuth = value.to(u.deg)


class SimulatedShower(CheckedShower):
    """An example of extended class
    """

    _attributes = CheckedShower._attributes + ["simulation",]


    def __init__(self, **kwargs):
        self.__simulation: Optional[str] = None

        super().__init__(**kwargs)


    @property
    def simulation(self) -> str:
        """The simulation tag"""
        return self.__simulation

    @simulation.setter
    def simulation(self, value: str):
        self._assert_not_set(self.__simulation)
        self.__simulation = value
