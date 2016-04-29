# Parkr
UIC CS course CS581's Search for Spatio Temporal Resources course project. This project is implemented in Python 3.

### Installing packages
Install packages given in the requirements.txt file. Simply run

<code>pip3 install -r requirements.txt</code>

or alternatively, if you only have one instance of Python (being Python 3), run

<code>pip install -r requirements.txt</code>

Sometimes, there are path issues that prevent the system from seeing pip as a system wide command, in such cases, run

<code>python3 -m pip install -r requirements.txt</code>

### Running Simulations
In order to run a simulation, run the `simulate.py` script. This script will require a simulation input file, similar to the one that can be found at `simulations/simulation_input.csv`. Newer simulation inputs can be generated using the `generate_inputs.py` running it as below

<code>python3 generate_inputs.py 100 simulations/simulation_input.csv</code>

The above script generates 100 random inputs in a file called `simulations/imulation_input.csv`

You can run `simulate.py` as below

<code>python3 simulate.py -a d -i input_file.csv -o output_file.csv -c 10 -s 1</code>

__Note:__ The above command line inputs will generate a simulation results file called output_file.csv for the deterministic grav pull algorithm (d - deterministic, p - probabilistic) where the real time data used with a congestion of 10% and a sampling rate of 1 (which means that the algorithm will be executed at every intersection). The congestion argument takes a default value of 0 and the sampling rate argument takes a default value of 1 if omitted. A congestion value of anything other than 0, 10, 30 or 60 will make the simulation run longer because the algorithm needs to generate a new randomized file of the real time data with the congestion introduced. For any congestion value of 0, 10, 30 or 60, the input file with some random congestion has already been generated and hence this computation can be skipped

Typing 

<code>python3 simulate.py --help</code>

will display the list of command line options and what values are expected.
