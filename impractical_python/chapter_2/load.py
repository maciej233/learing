"""Load file"""
import sys
import os

def load(file):
    try:
        with open(file, 'r') as f:
            loaded_text = f.read().strip().split('\n')
            loaded_text = [x.lower() for x in loaded_text]
            f.close()
            return loaded_text
    except IOError as e:
        print(f"{e}\nError opening {file}. Error Terminging", file=sys.stderr)
        sys.exit(1)