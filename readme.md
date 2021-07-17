# SpellChecker and SpellCorrector
Version 1.0

Author: Tzoop Ilya (ilyatzoop@gmail.com)

## Description
This application is a console version of a `SpellCorrector` app, which supports all languages of the world.
As a dictionaries for testing there are Russian and English dictionaries available.
You can also create your own dictionary from a text file for any language through `dictionary_creator.py`


## Requirements
* Python >= 3.6


## Content
* Console SpellCorrector: `spellcorrector.py`
* Console Dictionary Creator: `dictionary_creator.py`
* Console Dictionary Downloader: `dictionary_downloader.py`
* Modules: `SpellCorrector/`
* Tests: `Tests/`
* Used dictionaries: `Correct Dictionaries`


## SpellCorrector
Has 2 modes:
* 1) Mispellings
Prints all mistakes in the following format: `line:index` {'word': 'WORD'`, 'correction': ['CORR1', 'CORR2']`}
* 1.1) [-c], [--coordinate] - Adds coordinate `line:index` to the output
* 1.2) [--correct] amount - Corrects `amount` of mistakes and prints them
* 2) Mistake Finder
Prints all mistakes in the following format without coordinates and corrections
Example: `./spellcorrector.py --infile Texts\HarryPotterText.txt mistake_finder 10`
More detailed information is available with `--help` flag.


## Dictionary Creator
Allows you to work with dictionaries.
Has 4 modes:
* 1) Add
Adds a word to the chosen dictionary. (You can't just open the dictionary and append a word. A special hash `salt` is used to prevent corruption and keep words in the desired format.)
* 2) Append
Appends second dictionary to the first
* 3) Merge
Merges two dictionaries and stores them as a separate dictionary
* 4) Create
Creates a dictionary from a provided text file.
Example: `./dictionary_creator.py add Zeliboba "Correct Dictionaries/large.dic"`
There is also `--help` available.

## Dictionary Downloader
Downloads Russian and English dictionaries and stores them in the `Correct Dictionaries` folder.
Launch: `./dictionary_downloader.py`


## Implementation details
Supports line breaks, skipped spaces, mispellings.
Based on Levenshtein distance metric.
Module, calculating Levenshtein distance, is located here: `SpellCorrector/levenshtein_distance_counter.py`
This module is based on a Trie for fast distance calculation. There is also an heuristic optimization for the same purpose.

