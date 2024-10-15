import time, csv, os
import pandas as pd
import numpy as np

N_ITERS = 10
FILTER_MIN = 0.25
FILTER_MAX = 0.75
N_ROWS = [10,100,1000, 10000, 100000]
N_COLS = [5, 10, 20]

RESULTS_FILE = os.path.relpath("Results/np_vs_pd_times.csv")

def make_random_dict(n_rows, n_cols)->dict:
    _dict={}
    for i in range(n_cols):
        key = f"col_{i}"
        _dict[key] = np.random.rand(n_rows)
    return _dict

def are_equiv(d:dict, df:pd.DataFrame):
    """
    Check to see if a data frame and np dict are equivalent 
    """
    for key in d.keys():
        if any(df[key] != d[key]): return False

    return True


if __name__ == "__main__":
    np_time = 0
    df_time = 0
    f = open(RESULTS_FILE, mode="w", newline="")
    writer=csv.writer(f)
    writer.writerow(["n_rows", "n_cols", "np_time", "df_time"])
    for r in N_ROWS:
        for c in N_COLS:
            for _ in range(N_ITERS):
                # Make dict and df
                np_dict = make_random_dict(r,c)
                df = pd.DataFrame(np_dict)

                # Ensure dict and df are equivalent 
                assert(are_equiv(df,np_dict))

                # Time np filtering 
                _t = time.time()
                mask = [n >= FILTER_MIN and n <= FILTER_MAX for n in np_dict['col_0']]
                for k in np_dict.keys():
                    np_dict[k] = np_dict[k][mask]
                np_time += time.time()-_t

                # Time df filtering 
                _t = time.time_ns()
                df = df[df['col_0'].between(FILTER_MIN, FILTER_MAX, inclusive='both')]
                df_time += (time.time_ns()-_t)/(10**9)

                # Ensure dict and df remain equivalent after filtering 
                assert(are_equiv(df,np_dict))

            np_time/N_ITERS
            df_time/N_ITERS

            writer.writerow([r, c, np_time, df_time])

    f.close()
