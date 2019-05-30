import argparse
import glob
import os
# import time

from modified import find_modified


def parse_args() -> str:
    """
    parsing cli parameters to find required one 'path'
    :return: path value from args
    """
    parser = argparse.ArgumentParser(description='First test task on images similarity.')
    parser.add_argument('--path', help='PATH', type=str, required=True)
    args = parser.parse_args()

    return vars(args)['path']


if __name__ == '__main__':
    path = parse_args()  # getting path from cli

    all_files = glob.glob(os.path.join(path, '*.*'))
    # curr = time.time()

    # calling function to calculate duplicate and modified images
    modified = find_modified(all_files)

    # printing results
    print('\n'.join([' '.join([os.path.basename(y) for y in x]) for x in modified]))

    # print("{:.2f}".format(time.time() - curr) + ' seconds')
