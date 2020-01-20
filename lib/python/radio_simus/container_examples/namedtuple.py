from collections import namedtuple

"""Example of raw shower container

1. It is a tuple, i.e. it is immutable. Attributes can only be set at init.
   They can't be modfied afterwards. Note that there are extra packages on PyPI
   that provide mutable named containers, e.g. `recordclass`.

2. The fields can be accessed as a tuple or as attributes, e.g. `shower.energy`.

3. There is no cross-check when getting or setting a field.

4. All atributes are set to optionnal by providing default values.
"""
RawShower = namedtuple("RawShower",
                       ("showerID", "primary", "energy", "zenith", "azimuth"),
                       defaults = 5 * (None,))


import astropy.units as u
from typing import NamedTuple, Optional

"""Example of staticaly typed shower

1. As previously, it is an immutable container. The fields can be accessed as a
   tuple or as attributes.

2. There is no runtime cross-check when getting or setting a field. However,
   you can run a static analyzer like `mypy` in order to detect wrong type
   usages.  Note that while the static check can ensure that a field, e.g. the
   energy, is an astropy.Quantity (i.e. has a unit), it can not check for a
   specific unit.  E.g. the energy can be given with unit meters.

3. All atributes are set to optionnal using the explicit `Optional` type.
"""
class TypedShower(NamedTuple):
    """Represents a particle shower"""
    showerID: Optional[str] = None
    primary: Optional[str] = None
    energy: Optional[u.Quantity] = None
    zenith: Optional[u.Quantity] = None
    azimuth: Optional[u.Quantity] = None
