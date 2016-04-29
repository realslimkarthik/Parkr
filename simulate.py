import argparse
import os
import sys
from algorithms import run_simulation


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--algo', help='The algorithm to run on the simulation file. Should be one \
        of \'d\' or \'p\'', required=True)
    parser.add_argument('-i', '--input_file', help='The name of the input simulation file', required=True)
    parser.add_argument('-o', '--output_file', help='The name of the file to write the output simulation data', required=True)
    parser.add_argument('-c', '--congestion', help='The congestion percentage for this algorithm', default=0, type=int)
    parser.add_argument('-s', '--sampling_rate', help='The number of times to re-execute the algorithm in a \
         single simulation run', default=1, type=int)

    args = parser.parse_args()

    algo = args.algo
    if algo != 'd' and algo != 'p':
        print('Algorithm should be either \'d\' or \'p\'')
        sys.exit(1)
    input_file = args.input_file
    output_file = args.output_file
    congestion = args.congestion
    sampling_rate = args.sampling_rate

    if not os.path.isfile(input_file):
        print('The input file that you passed does not exist')
        sys.exit(1)

    if not os.path.isfile(output_file):
        print('The output file that you passed does not exist')
        sys.exit(1)

    run_simulation(algo, input_file, sampling_rate, congestion, output_file)


if __name__ == '__main__':
    main()