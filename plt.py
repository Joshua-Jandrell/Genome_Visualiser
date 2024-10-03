"""
Contains simple functions to generate random vcf data for plot speed testing.
"""

import numpy as np
import matplotlib as mpt
import matplotlib.pyplot as plt

def get_random_zygoisty(n_variants:int=5000, n_samples:int=500, value_range:tuple[int, int]=(-1, 2)):
    """
    Creates a random zygositiy matrix with the given dimensions
    """
    dummy = np.random.random_integers(0, value_range[1], (n_variants, n_samples))
    dummy[0,0] = -1
    dummy[-1,-1] = -1
    return dummy


BLOCK_SIZE = 20
BAR_PAD = 2


if __name__ == "__main__":
    # get frequency
    case = get_random_zygoisty(n_variants=60, n_samples=30)
    n_rows, n_cols = case.shape
    print(case)
    print(n_rows)
    hom_freq = [sum([val == 2 for val in row])/n_cols for row in case]
    het_freq = [sum([val == 1 for val in row])/n_cols for row in case]


    y_pos = np.arange(n_rows)
    plt.barh(y_pos, hom_freq, align='center', color='yellow')
    plt.barh(y_pos, het_freq, left=hom_freq, align='center', color='green')

    ctrl = get_random_zygoisty(n_variants=60, n_samples=30)
    hom_freq_2 = np.array([-1*sum([val == 2 for val in row])/n_cols for row in ctrl])
    het_freq_2 = np.array([-1*sum([val == 1 for val in row])/n_cols for row in ctrl])

    plt.barh(y_pos, hom_freq_2, align='center', color='orange')
    plt.barh(y_pos, het_freq_2, left=hom_freq_2, align='center', color='lightgreen')

    plt.plot([0,0], [0,n_rows], color='black')

    plt.show()

    plt.clf()

    width=10

    plt.barh(y_pos+0.25, hom_freq, 0.4, align='center', color='yellow')
    plt.barh(y_pos+0.25, het_freq, 0.4, left=hom_freq, align='center', color='green')

    plt.barh(y_pos-0.25, -1*hom_freq_2, 0.4, align='center')
    plt.barh(y_pos-0.25, -1*het_freq_2, 0.4, left=-1*hom_freq_2, align='center')

    plt.show()