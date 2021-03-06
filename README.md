# Parkr
UIC CS course CS581's Search for Spatio Temporal Resources course project for Team 4 that consists of 
  
  * Ayush Chugh (achugh4)
  * Karthik Hariharan (kharih2)
  * Kiran Sheena Marakala (ksheen3)


### Installing packages
Install packages given in the requirements.txt file. Simply run

`pip3 install -r requirements.txt`

or alternatively, if you only have one instance of Python (being Python 3), run

`pip install -r requirements.txt`

Sometimes, there are path issues that prevent the system from seeing pip as a system wide command, in such cases, run

`python3 -m pip install -r requirements.txt`


### Adding a Google Maps key
Generate a Google Maps API key (ideally a server key) and enable Directions and Distance Matrix APIs on the Google API manager. Once the key has been generated, update the `api_keys` list in the 2nd line of the `credentials.py` file by adding the newly generated API Key as a string like so

`api_keys = ['<YOUR_API_KEY_HERE>]'`


### Running a Simulation on the browser
After installing the necessary packages, you can run the web server by typing the following command on a command prompt/terminal

`python3 parkr.py`

This above command will start a web server that is listening for incoming connection requests on port 5000 of the localhost, so going to `http://localhost:5000` on the browser will open the web page. After entering the corresponding inputs, the server will compute the best parking spot (this may take upto a minute) and the route and it will be displayed on the web page as shown below.

![Web Page Simulation](https://raw.githubusercontent.com/realslimkarthik/Parkr/master/Web_Page_Screenshot.png "Browser Simulation")

### Running Simulations Command Line
In order to run a simulation, run the `simulate.py` script. This script will require a simulation input file, similar to the one that can be found at `simulations/simulation_input.csv`. Newer simulation inputs can be generated using the `generate_inputs.py` running it as below

`python3 generate_inputs.py 100 simulations/simulation_input.csv`

The above script generates 100 random inputs in a file called `simulations/imulation_input.csv`

You can run `simulate.py` as below

`python3 simulate.py -a d -i input_file.csv -o output_file.csv -c 10 -s 1`

__Note:__ The above command line inputs will generate a simulation results file called output_file.csv for the deterministic grav pull algorithm (d - deterministic, p - probabilistic) where the real time data used with a congestion of 10% and a sampling rate of 1 (which means that the algorithm will be executed at every intersection). The congestion argument takes a default value of 0 and the sampling rate argument takes a default value of 1 if omitted. A congestion value of anything other than 0, 10, 20, 30 or 60 will make the simulation run longer because the algorithm needs to generate a new randomized file of the real time data with the congestion introduced. For any congestion value of 0, 10, 20, 30 or 60, the input file with some random congestion has already been generated and hence this computation can be skipped

Typing 

`python3 simulate.py --help`

will display the list of command line options and what values are expected.
