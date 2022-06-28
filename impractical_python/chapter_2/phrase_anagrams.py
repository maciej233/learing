"""The the program find anagrams phrases from user choice."""
import sys
from collections import Counter
import load

FILE = "2of4brif.txt"
WORD_LIST = load.load(FILE)
WORD_LIST.append('i')
WORD_LIST.append('a')
WORD_LIST = sorted(WORD_LIST)

INIT_NAME = input("Give a name: ")

def find_anagrams(name, word_list):
    """Find anagrams from list."""
    name_letter_map = Counter(name.lower())  # Counter the given name
    anagrams = []  # store anagrams

    for word in word_list:  # loop for dict
        word_letter_map = Counter(word.lower())
        test = ''
        for letter in word:
            if word_letter_map[letter] <= name_letter_map[letter]:
                test += letter
        if Counter(test) == word_letter_map:
            anagrams.append(word)
    print(*anagrams, sep='\n')
    print()
    print(f"Reaming letters {name}", file=sys.stderr)
    print(f"Number of remaming letters {len(name)}")
    print(f"Number of remaing real word anagrams {len(anagrams)}")

def main():
    pass

def user_choice(name):
    while True:
        left_over_list = list(name)
        user_choice = input("\nGive or choice to start or '#' to end")
        if user_choice == '':
            main()
        elif user_choice == '#':
            sys.exit()
        else:
            candidate = ''.join(user_choice.lower().split())
        for letter in candidate:
            if letter in left_over_list:
                left_over_list.remove(letter)
        if len(name) - len(left_over_list) == len(candidate):
            break
        else:
            print("WONT WORK! Try another choices", file=sys.stderr)
    name = ''.join(left_over_list)
    return user_choice, name
