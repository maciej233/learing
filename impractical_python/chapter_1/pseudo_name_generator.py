"""Generate FUNNY NAMES from combing 2 seperate lists."""
import random
import sys

def main():
    """Główna Funckja."""
    names = ["Janek", "Grzesiek", "Jakub"]
    surnames = ["Mucha", "Robak", "Kozel"]
    while True:
        name = random.choice(names)
        surname = random.choice(surnames)
        print("lets play the game\ndrow by lot a funny person")
        print(f"{name} {surname}\n".format(file=sys.stderr))
        user_choice = input("Do you want to play again (y/n)")
        if user_choice == "n".lower():
            break

if __name__ == "__main__":
    main()
