#!/usr/bin/env python3

INSERT_COST = 1
DELETE_COST = 1
REPLACE_COST = 1


class TrieNode:
    def __init__(self):
        self.word = False
        self.children = {}


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert_word(self, word):
        node = self.root
        for letter in word:
            if letter not in node.children:
                node.children[letter] = TrieNode()
            node = node.children[letter]
        node.word = True


def load_dictionary(filename):
    trie = Trie()
    with open(filename, 'r', encoding='utf8') as dictionary:
        for word in dictionary:
            word = word.rstrip()
            trie.insert_word(word)
    return trie


def count_new_row(previous_row, needle, new_letter):
    current_row = [previous_row[0] + 1]
    for column in range(1, len(needle) + 1):
        insert_value = current_row[column - 1] + INSERT_COST
        delete_value = previous_row[column] + DELETE_COST
        if needle[column - 1] == new_letter:
            replace_value = previous_row[column - 1]
        else:
            replace_value = previous_row[column - 1] + REPLACE_COST
        levenshtein_distance = min(insert_value, delete_value, replace_value)
        current_row.append(levenshtein_distance)
    return current_row


def count_table_recursively(trie, needle, max_levenshtein_value, previous_row, current_word, result):
    current_row = count_new_row(previous_row, needle, current_word[-1])
    if current_row[-1] <= max_levenshtein_value and trie.word:
        result.append((current_word, current_row[-1]))
    if min(current_row) <= max_levenshtein_value:
        for letter in trie.children:
            count_table_recursively(trie.children[letter], needle, max_levenshtein_value, current_row,
                                    current_word + letter, result)


def find_possible_replacements(trie, needle, max_levenshtein_value):
    possible_replacements = []
    first_row = range(len(needle) + 1)
    for letter in trie.root.children:
        count_table_recursively(trie.root.children[letter], needle,
                                max_levenshtein_value, first_row, letter, possible_replacements)
    return possible_replacements


def is_word_in_dictionary(trie, needle):
    current_node = trie.root
    for letter in needle:
        if letter in current_node.children:
            current_node = current_node.children[letter]
        else:
            return false
    return current_node.word
