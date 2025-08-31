# path_handler.py

import os
import sys

def get_data_path(file_name):
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
        return os.path.join(base_path, 'data', file_name)
    else:

        base_path = os.path.abspath(os.path.dirname(__file__))
        return os.path.join(base_path, 'data', file_name)

