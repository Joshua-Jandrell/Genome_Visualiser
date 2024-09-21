"""
Contains simple functions to generate random vcf data for plot speed testing.
"""

import numpy as np

def get_random_zygoisty(n_variants:int=5000, n_samples:int=500, value_range:tuple[int, int]=(-1, 2)):
    """
    Creates a random zygositiy matrix with the given dimensions
    """
    dummy = np.random.random_integers(0, value_range[1], (n_variants, n_samples))
    dummy[0,0] = -1
    dummy[-1,-1] = -1
    return dummy





if __name__ == "__main__":
    print(get_random_zygoisty(20, 5))