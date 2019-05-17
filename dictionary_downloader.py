#!/usr/bin/env python3

from pathlib import Path
import sys
import os.path
import urllib.request

path_to_save = Path("Correct Dictionaries")
if not os.path.exists(path_to_save):
    os.mkdir(path_to_save)
try:
    urllib.request.urlretrieve(
        "https://transfer.sh/hJZLV/russian.dic", path_to_save / "russian.dic")
    urllib.request.urlretrieve(
        "https://transfer.sh/UvndF/large.dic", path_to_save / "large.dic")
except Exception as e:
    print('Files not found. Probably they were deleted: "{}"'.format(e), file=sys.stderr)
