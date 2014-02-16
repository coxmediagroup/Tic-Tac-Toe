# Usage: ROOT('templates/')
import os

ROOT = lambda base : os.path.abspath(
    os.path.join(
        os.path.dirname(__file__), base
    ).replace('\\','/')
)

ROOT_DIR = os.path.dirname(__file__)