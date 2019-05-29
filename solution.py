import argparse
import numpy as np

parser = argparse.ArgumentParser(description='First test task on images similarity.')
parser.add_argument('--path', help='PATH', type=str, required=True)
args = parser.parse_args()

print(args)
