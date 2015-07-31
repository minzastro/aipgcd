#!/usr/bin/python
import healpy
import numpy as np
from astropy.io import fits


def uniq(value):
    """
    Convert from NUNIQ HEALPix coding method used for MOCs into
    order-index pairs.
    See http://www.ivoa.net/documents/MOC/20130910/WD-MOC-1.0-20130910.html
    for details.
    """
    order = int(np.log2(value/4)/2)
    npix = value - 4 * (4**order)
    return order, npix

def cell_area(level):
    return (129600. / np.pi) * 4**(-level) / 12.

class MOCFinder(object):
    """
    Class to search for positions in HEALPix Multi-Order Coverage maps.
    See http://www.ivoa.net/documents/MOC/20130910/WD-MOC-1.0-20130910.html
    MOCs can be prepared with Aladin or stilts or downloaded from
    http://alasky.u-strasbg.fr/footprints/tables/vizier/
    """
    def __init__(self, filename, moc_name=''):
        """
        filename - FITS file containing MOC map.
        """
        self.moc_name = moc_name
        self.fitstbl = fits.open(filename)[1]
        self.healpix = {}
        for row in self.fitstbl.data:
            order, npix = uniq(row[0])
            if order not in self.healpix:
                self.healpix[order] = []
            self.healpix[order].append(npix)

    def is_in(self, ra, decl):
        """
        Check if position is in the MOC map.
        ra, decl - sky coordinates (or lists of coordinates).
        """
        theta = 0.5*np.pi - np.radians(decl)
        phi = np.radians(ra)
        keys = self.healpix.keys()
        keys.sort()
        if isinstance(ra, float):
            for level in keys:
                healpix_cell = healpy.ang2pix(2**level, theta, phi, nest=True)
                if healpix_cell in self.healpix[level]:
                    return True
            return False
        else:
            result = np.zeros(len(ra), dtype=bool)
            for level in keys:
                healpix_cell = healpy.ang2pix(2**level, theta, phi, nest=True)
                cellcheck = [cell in self.healpix[level] for cell in healpix_cell]
                if cellcheck.any():
                    result = result + cellcheck
                if result.all():
                    return result
            return result


    def get_area(self):
        area = 0.
        for level in self.healpix.keys():
            area = area + cell_area(level) * len(self.healpix[level])
        return area

if __name__ == '__main__':
    moc_finder = MOCFinder('../data/MOC_sdss.fits')
    print moc_finder.is_in(270., 24.)
