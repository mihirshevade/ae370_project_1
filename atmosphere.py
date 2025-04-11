from pyatmos import coesa76
import numpy as np

def atmosphere_properties(altitude):
    props = coesa76(altitude / 1000)
    a = np.sqrt(1.4 * 287 * props.T)
    return props.rho, props.T, a