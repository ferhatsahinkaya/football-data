from footballapi.api import FootballApi
from match.topbottompercent import TopBottomPercent


def main():
    for competition in FootballApi.get_competitions():
        print(TopBottomPercent.get_matches(competition))


if __name__ == "__main__":
    main()
