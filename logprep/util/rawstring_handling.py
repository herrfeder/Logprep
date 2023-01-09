""" module for rawstring handling helper methods"""
import os
from typing import List

from yaml import safe_dump

def parse_rawstring(file_path: str):
    """
    Reads and parses one json file and return it as list, containing either only one json or
    multiple jsons depending on the file.

    Parameters
    ----------
    file_path: str
        Path to the json file.

    Returns
    -------
    list
        A list of dictionaries representing the json/jsons.
    """
    with open(file_path, "r", encoding="utf8") as log_file:
        log_lines = log_file.read()
        return log_lines

