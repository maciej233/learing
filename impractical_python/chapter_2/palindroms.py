"""FIND PALINDROMS and PALINGRAMS FROM THE LIST"""
import load


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

def clean_up_dict(list):
    """Clean the final list from single letters."""
    word_list = ["a", "nurses", "i", "stack", "b", "cats", "c", "h"]
    permissions = ["a", "i"]
    for word in word_list:
        if len(word) == 1 and word not in permissions:
            if word in list:
                list.remove(word)
    return list


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
    palingrams = clean_up_dict(palingrams)
    return palingrams

def find_palingrams_optimalized(file):  # 0.4s faster due to set instead of
    """find alingrams from a list."""
    source = load.load(file)
    source = set(source)
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