#!/usr/bin/env python

from multiprocessing import Pool
import argparse
import os
import subprocess

parser = argparse.ArgumentParser(description='Draco my Tiles++')
parser.add_argument('input_folder', metavar='input-folder', help='A folder containing .b3dm files')
parser.add_argument('output_folder', metavar='output-folder', help='A folder where the comprssed tiles will be written')
parser.add_argument('--concurrency', metavar='N', type=int, default=10, help='Concurrency level')
    
args = parser.parse_args()

def process_file(data):
    input_file, output_file = data
    result = subprocess.run(
                [
                    'node',
                    'bin/3d-tiles-tools.js',
                    '-f', 
                    'bakeB3dm',
                    '-i', 
                    input_file,
                    '-o', 
                    output_file
                ],
                stdout=subprocess.PIPE
            )

    if "ERROR" in str(result.stdout):
        print("FAILED: {}".format(input_file))
    else:
        print(output_file)

if __name__ == '__main__':
    work = []
    for file in sorted(os.listdir(args.input_folder)):
        if file.endswith(".b3dm"):
            full_path = os.path.join(args.input_folder, file)
            output_path = os.path.join(args.output_folder, file)
            work.append((full_path, output_path))

    print("Running pool with {} workers".format(args.concurrency))
    pool = Pool(args.concurrency)
    pool.map(process_file, work)
