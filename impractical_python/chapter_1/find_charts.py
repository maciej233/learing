"""Program finds chars in sentece and display the amount of specific char."""
from pprint import pprint
from collections import defaultdict
import sys
def main():
    """Głowna funckja."""
    ALPHABET = 'abcdefghijklmnopqrstuvwxyz'
    text = "This is my example sentece to exam the amount of charatcters in"
    result = defaultdict(list)
    result = {letter.lower(): [] for letter in ALPHABET}
    for char in text:
        char = char.lower()
        if char in ALPHABET:
            result[char].append(char)
    print("{}".format(text), file=sys.stderr)
    pprint(result, width=110)


if __name__ == '__main__':
    main()
