import argparse
import logging

from footballapi import footballapi
from match import filtermatch

logger = logging.getLogger()
logger.setLevel(logging.INFO)
parser = argparse.ArgumentParser(description='Finds matches according to given query')
parser.add_argument('--topbottompercent', dest='topbottompercent', type=int, choices=range(1, 101), default=100,
                    help='Finds matches between top and bottom x percent teams')

args = parser.parse_args()


def main():
    print(args)
    for competition in footballapi.get_competitions():
        logger.info(
            filtermatch.get_matches(competition, {'type': 'topbottompercent', 'percentage': args.topbottompercent}))


if __name__ == "__main__":
    main()
