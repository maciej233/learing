import argparse
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("person")
    args = parser.parse_args()
    print(f"hello sexy person {args.person}")

if __name__ == "__main__":
    main()

