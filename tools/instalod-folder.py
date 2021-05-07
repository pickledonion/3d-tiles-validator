#!/usr/bin/env python

from multiprocessing import Pool
import argparse
import os
import subprocess

parser = argparse.ArgumentParser(description='InstaLOD my Tiles++')
parser.add_argument('profile', metavar='json file', help='File name of the InstaLOD profile')
parser.add_argument('input_folder', metavar='input-folder', help='A folder containing .b3dm files')
parser.add_argument('output_folder', metavar='output-folder', help='A folder where the comprssed tiles will be written')
parser.add_argument('--concurrency', metavar='N', type=int, default=1, help='Concurrency level')
parser.add_argument('--blender-path', metavar='path', type=str, default='C:\\Program Files\\Blender Foundation\\Blender 2.92\\blender.exe', help='Path to blender.exe')
parser.add_argument('--instalod-path', metavar='path', type=str, default='C:\\Apps\\InstaLODPipeline_2020b\\InstaLODCmd.exe', help='Path to InstaLODCmd.exe')

    
args = parser.parse_args()

def process_file(data):
    input_file, output_file, profile, blender_path, instalod_path = data
    
    result = subprocess.run(
                [
                    'node',
                    'bin/3d-tiles-tools.js',
                    '-b',
                    blender_path,
                    '-l',
                    instalod_path,
                    '-f', 
                    'instaLODB3dm',
                    '-i', 
                    input_file,
                    '-o', 
                    output_file,
                    '--options' ,
                    profile
               
                ],
                stdout=subprocess.PIPE
            )

    if "ERROR" in str(result.stdout):
        print("FAILED: {}".format(input_file))
        print(result.stdout)
    else:
        print('{} ({})'.format(output_file,profile))

if __name__ == '__main__':
    work = []
    for file in sorted(os.listdir(args.input_folder)):
        if file.endswith(".b3dm"):
            full_path = os.path.join(args.input_folder, file)
            output_path = os.path.join(args.output_folder, file)
            work.append((full_path, output_path, args.profile, args.blender_path, args.instalod_path))

    print("Running pool with {} workers".format(args.concurrency))
    pool = Pool(args.concurrency)
    pool.map(process_file, work)
