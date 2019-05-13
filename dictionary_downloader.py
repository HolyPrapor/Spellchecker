#!/usr/bin/env python3

from pathlib import Path
import urllib.request

path_to_save = Path("Correct Dictionaries")
urllib.request.urlretrieve(
    "https://transfer.sh/hJZLV/russian.dic", path_to_save / "russian.dic")
urllib.request.urlretrieve(
    "https://transfer.sh/116RrA/large.dic", path_to_save / "large.dic")
