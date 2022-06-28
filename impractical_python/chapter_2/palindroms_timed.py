"""FIND PALINDROMS and PALINGRAMS FROM THE LIST"""
import load
import time

start = time.time()
def find_palindroms(file):
    """Find palindroms from a list."""
    source = load.load(file)
    palindroms = []

    for word in source:
        if len(word) > 1 and word == word[::-1]:
            palindroms.append(word)
    print(f"\nThis is a list of palindorms\n{len(palindroms)}")
    print(*palindroms, sep='\n')
    return palindroms

def find_palingrams(file):
    """find alingrams from a list."""
    source = load.load(file)
    palingrams = []
    for word in source:
        reversed_word = word[::-1]
        if len(word) > 1:
            for index, letter in enumerate(word):
                if word[index:] == reversed_word[:index] and reversed_word[index:] in source:
                    palingrams.append((word, reversed_word[index:]))
                if word[:index] == reversed_word[index:] and reversed_word[:index] in source:
                    palingrams.append((reversed_word[:index],word))
    palingrams = sorted(palingrams)
    print(f"\nThis is a list of palindroms\n{len(palingrams)}")
    for first, second in palingrams:
        print(f"{first} {second}")
    return palingrams

end = time.time()

print(f"The time of running program is {end - start}")