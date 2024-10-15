import time, tracemalloc, gc
from typing import Callable

def monitor_time(fxn:Callable, n_runs = 10)->list[float]:
    """
    Monitor time only.
    """
    _times = []
    for _ in range(n_runs):
        # Start tracking memory 
        _start_time = time.time()
        fxn()
        _end_time = time.time()-_start_time
        _times.append(_end_time)  

    return _times

def monitor_memory(fxn:Callable, n_runs = 10)->tuple[list[float], list[float]]:
    _mems = []
    _peak_mems = []
    for _ in range(n_runs):
        tracemalloc.start()
        fxn()
        _mem, _peak_meme = tracemalloc.get_traced_memory()
        _mems.append(_mem)
        _peak_mems.append(_peak_meme)
        tracemalloc.stop()
        gc.collect()
    return _mems, _peak_mems
    
def monitor_time_and_mem(fxn:Callable, n_runs = 10):
    """
    Monitors both time and memory of a function. \n
    Returns values in the form time, memory used, peak memory used.
    Note these must be tracked separately to avoid errors and inaccuracies.
    """
    times = monitor_time(fxn=fxn, n_runs=n_runs)
    mem, peaks = monitor_memory(fxn=fxn, n_runs=n_runs)
    return times, mem, peaks

