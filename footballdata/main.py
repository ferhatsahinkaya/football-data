from footballapi import footballapi
from match import match


def main():
    for competition in footballapi.get_competitions():
        print(match.get_matches(competition, None))


if __name__ == "__main__":
    main()
