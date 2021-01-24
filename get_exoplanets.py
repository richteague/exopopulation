from astroquery.open_exoplanet_catalogue import findvalue
from astroquery import open_exoplanet_catalogue as oec
import numpy as np


def get_exoplanets(output='exoplanets.txt'):
    """Grabs all planets from Open Exoplanet Catalogue and saves them."""
    cata = oec.get_catalogue()
    planets = []
    for planet in cata.findall(".//planet"):
        smax = findvalue(planet, 'semimajoraxis')
        mass = findvalue(planet, 'mass')
        year = findvalue(planet, 'discoveryyear')

        # remove those entries which aren't complete
        if mass is None or smax is None or year is None:
            continue

        # remove solar system bodies
        if year.value < 1990.0:
            continue

        planets += [[mass.value, smax.value, year.value]]

    planets = np.array(planets).astype(float)
    header = 'mass (Mjup), semi-major axis (au), discovery year'
    np.savetxt(output, planets, header=header, fmt='%.4e')
    print('{} planets saved to {}.'.format(planets.shape[0], output))


if __name__ == "__main__":
    get_exoplanets()
