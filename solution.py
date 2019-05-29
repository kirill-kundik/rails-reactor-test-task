import argparse
import glob
import hashlib
import os


# import numpy as np
# from PIL import Image


def parse_args():
    parser = argparse.ArgumentParser(description='First test task on images similarity.')
    parser.add_argument('--path', help='PATH', type=str, required=True)
    args = parser.parse_args()

    return vars(args)['path']


if __name__ == '__main__':
    path = parse_args()

    all_files = glob.glob(os.path.join(path, '*.jpg'))

    duplicates = dict()

    for infile in all_files:
        with open(infile, 'rb') as input_file:
            file_hash = hashlib.sha3_256(input_file.read()).hexdigest()

            if file_hash not in duplicates:
                duplicates[file_hash] = [os.path.basename(infile)]
            else:
                duplicates[file_hash].append(os.path.basename(infile))

    for k, v in duplicates.items():
        if len(v) > 1:
            print(' '.join(v))
