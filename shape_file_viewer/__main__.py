import os
import pathlib
import sys
from argparse import ArgumentParser

# Add the module to the path.
sys.path.append(str(pathlib.Path(__file__).parent.parent.absolute()))

from shape_file_viewer.controllers.ViewerController import ViewerController


parser = ArgumentParser()
parser.add_argument('--path', type=str, help='Path to shape path.')

args = parser.parse_args()
path = os.path.realpath(args.path)
if os.path.exists(path):
    viewer_controller = ViewerController(path)
    viewer_controller.run()
else:
    print(f'Shape path not found: {path}')
