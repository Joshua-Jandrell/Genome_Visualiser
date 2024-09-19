"""
Contains simple functions to generate random vcf data for plot speed testing.
"""

import numpy as np

def get_random_zygoisty(n_variants:int=5000, n_samples:int=500, value_range:tuple[int, int]=(-1, 2)):
    """
    Creates a random zygositiy matrix with the given dimensions
    """
    return np.random.random_integers(value_range[0], value_range[1], (n_variants, n_samples))





if __name__ == "__main__":
    print(get_random_zygoisty(20, 5))