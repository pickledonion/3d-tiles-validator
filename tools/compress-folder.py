#!/usr/bin/env python

from multiprocessing import Pool
import argparse
import os
import subprocess
import sys

parser = argparse.ArgumentParser(description='Draco my Tiles++')
parser.add_argument('input_folder', metavar='input-folder', help='A folder containing .b3dm files')
parser.add_argument('output_folder', metavar='output-folder', help='A folder where the comprssed tiles will be written')
parser.add_argument('--concurrency', metavar='N', type=int, default=10, help='Concurrency level')
parser.add_argument('--basis', action='store_true' , help='Encode images to .basis')
parser.add_argument('--jpeg-quality', metavar='N', type=int, default=100, help='JPEG quality when encoding to JPEG')
parser.add_argument('--basis-quality', metavar='N', type=int, default=None, help='Basis quality when encoding to basis')
parser.add_argument('-v', '--verbose', action='store_true' , help='Verbose output for errors')
    
args = parser.parse_args()

def process_file(data):
    input_file, output_file = data
    result = subprocess.run(
                [
                    'node',
                    'bin/3d-tiles-tools.js',
                    '-f', 
                    'compressB3dm',
                    '-i', 
                    input_file,
                    '-o', 
                    output_file,
                    '--options' ,
                    '--jpeg-quality={}'.format(args.jpeg_quality) if args.jpeg_quality else '',
                    '--basis-quality={}'.format(args.basis_quality) if args.basis_quality else '',
                    '--basis' if args.basis else ''
                ],
                stdout=subprocess.PIPE
            )

    if "ERROR" in str(result.stdout):
        print("FAILED: {}".format(input_file))
        if args.verbose:
            print(result.stdout.decode())
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
