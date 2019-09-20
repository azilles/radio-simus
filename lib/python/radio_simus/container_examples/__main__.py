from .namedtuple import RawShower, TypedShower
from .property import CheckedShower

import astropy.units as u


if __name__ == "__main__":
    raw = RawShower(primary = "p", energy = 1E+19 * u.eV)
    print("This is a raw shower: ", raw)

    typed = TypedShower(primary = "Fe", energy = 1E+03 * u.m)
    print("This is a typed shower: ", typed)

    checked = CheckedShower(primary = "tau-", energy = 1E+00 * u.J)
    print("This is a checked shower: ", checked)
