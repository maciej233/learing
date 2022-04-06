"""This is simple ilustration how latin pig works."""

def main():
    """Give a word and get the latin pig version."""
    vovels = 'a', 'e', 'y', 'u', 'o'
    user_word = input("Give a word to convert: ")
    new_word = ''
    for i, word in enumerate(user_word):
        if user_word[0] in vovels:
            new_word = user_word + "way"
            break
        if word in vovels:
            new_word = user_word[i:] + user_word[:i] + 'ay'
            break
    print(new_word)

if __name__ == '__main__':
    main()
