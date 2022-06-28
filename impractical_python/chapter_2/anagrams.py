"""Find anagrams from the list."""
import load

FILE = "2of4brif.txt"

def find_anagrams(database):
    """Create list of anagrams: conforms user word with the list."""
    anagrams = []
    word_list = load.load(database)
    word_user = input("Give your word to find anagram: ")
    word_user = word_user.lower()
    word_user_sorted = sorted(word_user)
    for word in word_list:
        word = word.lower()
        word_sorted = sorted(word)
        if word != word_user:
            if word_sorted == word_user_sorted:
                anagrams.append(word)
    print("Anagrams = ", *anagrams, sep="\n")
    return anagrams

find_anagrams(FILE)
