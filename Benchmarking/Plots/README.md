# Plotting and Rendering Benchmark Tests
This directory contains scripts used to conduct plotting and rendering benchmarking tests.

The [Plot Tests](#plot-tests) are used to determine which [Matplotlib](https://matplotlib.org/) is the most effective (in terms of time and memory usage) for grid-based data visualisation.

The [Render Tests](#render-tests) are used to determine which plot display system works best to present and interactive plot in three [Custom Tkinter](https://github.com/TomSchimansky/CustomTkinter).

__________________________________________________________________________________________

# Plot Tests
The plot tests are conducted to investigate the absolute time duration and memory usage of various [Matplotlib](https://matplotlib.org/) plotting methods.

## Run Tests

> [!Warning]
> Running tests will override existing results.

To run the plot time and memory tests use the command (from the repo root):
```bash
python Benchmarking\Plots\runPlotTests.py
```
> [!TIP]
> These tests take a long time to complete.
> In may be more convenient to run time and memory tests separately or to edit the parameters in [`config.py`](config.py) to limit the number of test parameter/iterations.

Plot and memory tests are run independently to avoid the tracking method used in one from interfering with the measurement of the other.
As a result the `runPlotTests.py` can take tens of minute to complete. Tests can be run individually to reduce the continuous delay.

To track plotting time only use:
``` bash
python Benchmarking\Plots\timePlots.py
```

To track memory use only use:
```bash
python Benchmarking\Plots\trackPlotMemery.py
```
## Methodology
The following five Matplotlib plotting methods are investigated:

- [`pcolor`](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.pcolor.html) (Very slow: tested only for $50 \times 10$ at 100 DPI) 
- [`pcolorfast`](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.pcolorfast.html)
- [`pcolormesh`](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.pcolormesh.html)
- [`matshow`](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.matshow.html)
- [`imshow`](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.imshow.html)

These methods were selected because they can display grids of colored blocks: an important technique required to plot useful data visualisations such as heatmaps and color-coded variant-sample maps.
> [!NOTE]
> `pcolor` is significantly slower than all other methods and has thus been excluded from all tests to reduce testing time.

During testing each plot method is used to plot a randomly generated (NumPy) array of integers between `-1` and `2`. This array is intended to mimic the type of data plotted when generating the zygosity heat-map view.
Python code used to generate the arrays can be found in [`makeRandomData.py`](makeRandomData.py).

To investigate scalability, the impact of plot shape, and the affects of different DPIs: each plot method (excluding `pcolor`) is used to plot (randomly generated) data with various sample counts, variant counts and DPI values.

The values used are defined in the code snippet below:
``` python
# Code taken form Benchmarking\Plots\makeRandomData.pyconfig.py

VAR_COUNTS = [50, 500, 5000] # Variant counts used for benchmarking

SAMPLE_COUNTS = [10, 100, 1000, 10000] # Sample counts used for benchmarking

DPI_VALS = [50, 100, 150, 200] # DPI values used for benchmarking
```
The table below summarises the total number of blocks plotted when various combinations of samples and variants are used.
|Vars \ Samples |10|1 000|10 000|100 000|
|:---|:---:|:---:|:---:|:---:|
|50|500|5 000|50 000|500 000|5 000 000|
|500|5 000|50 000|500 000|5 000 000|
|5 000|50 000|500 000| 5 000 000| 50 000 000|

Each block is allocated a size of $10 \times 10$ pixels, regardless of DPI.

#### Measurement Techniques
Absolute wall-time is measured using the Python [`time`]( https://docs.python.org/3/library/time.html) library while memory allocation is tracked using the [`tracemalloc`]( https://docs.python.org/3/library/tracemalloc.html) library.

Each time/memory test is repeated ten times and averaged to improve reliability.

The python garbage collector ([`gc`]( https://docs.python.org/3/library/gc.html) is called between tests (and between each of the 10 repetitions). This ensures that a build-up of uncleared data( and the subsequent time-delay when the garbage collector is automatically called) does not affect test results.

## Verification
To verify that all plotting methods display data as desired each plotting method is used to plot a randomly generated $20 \times 10$ 'dataset' (essentially a random matrix).

The randomly generated data has only two white blocks (value of `-1`) placed in the top-left and bottom-right corner.
These blocks make it easier to ensure that the full dataset has been plotted and identify the orientation used by the plotting method.

> [!NOTE]
> `pcolor`, `pcolormesh` and `pcolorfast` all invert the y-axis causing the white blocks to appear in the bottom-left and top-right corners.

To run these verification tests use the bash command:
``` bash
python Benchmarking\Plots\verifyPlots.py
```
After the scrip has executed, `.png` images generated using each plot method will be saved in [`Results/Plots/ZygsityPlottingVerification`](../../Results/Plots/ZygsityPlottingVerification).
Each image follows the naming convention: `<name-of-plot-method>.png`.

> [!Warning]
> Running the `verifyPlots.py` will override any existing verification images and data.

These images can be inspected and compared to the random data used form plotting (sored in [`Results/Plots/ZygsityPlottingVerification/data.txt`](../../Results/Plots/ZygsityPlottingVerification/data.txt)) to verify that the plotting method displays data correctly.

The color mapping used by the plots is summarised in the table below:

| Color on plot | Data value |
|:--|:--|
|⬜ White | `-1`|
|🟦 Blue| `0`|
|🟩 Green|`1`|
|🟨 Yellow|`2`|

## Results
After the time and memory usage tests have been run, results can be found in [`Results/Plots/ZygsityPlotting/zygosity_plotting_times.csv`](../../Results/Plots/ZygsityPlotting/zygosity_plotting_times.csv`) and
[`Results/Plots/ZygsityPlotting/zygosity_plotting_memory.csv`](../../Results/Plots/ZygsityPlotting/zygosity_plotting_memory.csv`) respectively.
All time values are recorded in seconds and all memory usage values are recorded in bytes.

The results currently sored in the files (if no tests are run) were recorded on a Dell Inspiron laptop with an intel i7 core @ 1.7 GHz and 15.7 GB of usable RAM.
The computer was not used for any other tasks during benchmarking to ensure that changes in available resources did not impact test results.

By loading the plotting time results into the (to upload)MATLAB script, the following graphs were generated which show that :
*<small>Time taken for Matplotlib functions to plot different scales of randomly generated (NumPy) integer arrays </small>*
![time plots](https://github.com/user-attachments/assets/63eb544a-16fb-40cc-8657-74a5b4799264)

By loading the memory usage plotting results into the (to upload)MATLAB script, the following graphs were generated which show that :
*<small>Time taken for Matplotlib functions to plot different scales of randomly generated (NumPy) integer arrays </small>*
![memory usage plots](https://github.com/user-attachments/assets/e8aad650-ed6b-4f75-9aa5-5b0bd7d70bd2)

__________________________________________________________________________________________
# Render Tests
Render tests are conducted to identify which plot display system is the most appropriate in terms of absolute time (quantitative) and quality of display (qualitative).

Each plot display system must render a plot (data visualisation) and allow the user to scroll through this plot both vertically and horizontally.

## Run tests and methodology
To run the tests use the command:
```bash
python Benchmarking\Plots\runAppTests.py
```
This script will run three [Custom Tkinter](https://github.com/TomSchimansky/CustomTkinter) apps.
Each of th app will use one of three different system to display a plot (generated with [Matplotlib](https://matplotlib.org/)) in a [Custom Tkinter](https://github.com/TomSchimansky/CustomTkinter) app.

The plot display systems used are:
1. Plotting on a Matplotlib [TkAgg tkinter canvas](https://matplotlib.org/stable/api/backend_tk_api.html#matplotlib.backends.backend_tkagg.FigureCanvasTkAgg) and displaying the plot on a [CTkXYFrame](https://github.com/Akascape/CTkXYFrame).
2. Plotting on a Matplotlib [TkAgg tkinter canvas](https://matplotlib.org/stable/api/backend_tk_api.html#matplotlib.backends.backend_tkagg.FigureCanvasTkAgg) and enabling scrolling by re-setting plot limits in Matplotlib.
3. Saving the plot as an image which is then displayed using as a [Custom Tkinter Image](https://customtkinter.tomschimansky.com/documentation/utility-classes/image/) on a [CTkXYFrame](https://github.com/Akascape/CTkXYFrame) to enable scrolling.

> [!TIP]
> The display sysem used by an app will be indicated by its name.

> [!IMPORTANT]
> Custom Tkinter does not have a frame which can be scrolled in both x and y directions.
> The [CTkXYFrame](https://github.com/Akascape/CTkXYFrame) is an external object developed by Akash Bora ('Akascape`) and distributed under and [MIT licence](https://github.com/Akascape/CTkXYFrame/tree/main?tab=MIT-1-ov-file#).

Each of the plotting methods listen in the [Plot test: methodology](#Methodology) section is used generate a plot.

When the **plot next** button is clicked, the app will plot random data and display it. The size of the data generated ($500 \times 200$) and the Matplotlib plot method used will also be indicated.

The resercher is able to interact with the plot to see how well it scrolls before clicking the **clear plot** button to reset the Matplotlib figure and canvas.
Resetting the figure and canvas is important to ensure that all plot methods being with the same initial state: making benchmarking results comparable.

After then final plot method has been used the application will close and an apply using the next display system will open.

## Verification
The plot methods used are verified during the [Plot Tests](#plot-tests).
To ensure that the full plot is scrollable look for the two white blocks which should appear in the top-left and bottom-right OR top-right an bottom-left corners of the plot.

## Results 
The render tests do no generate results automatically.

Wall-times were recorded by videoing the applications and identifying the time that passed between clicking the **plot next** button and seeing a (correctly scaled) plot displayed. These times and qualitative observations were recorded in the (insert excel spreadsheet).
All tests were repeated three times to improve reliability.

The main findings were graphed in Excel which show that :
*<small>Time taken for Matplotlib functions to plot different scales of randomly generated (NumPy) integer arrays </small>*

![render times - smollr](https://github.com/user-attachments/assets/a9f71746-3165-4a55-b5e3-7264e502ada9)




