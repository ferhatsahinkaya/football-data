import argparse
import logging

from footballapi import footballapi
from match import filtermatch

logger = logging.getLogger()
logger.setLevel(logging.INFO)
parser = argparse.ArgumentParser(description='Finds matches according to given query')
group = parser.add_mutually_exclusive_group(required=False)
group.add_argument('-tbp', '--topbottompercent', dest='topbottompercent', type=int, choices=range(1, 101), default=100,
                   help='Finds matches between top and bottom x percent teams')
args = parser.parse_args()


def main():
    logger.info(args)
    if args.topbottompercent:
        filter = {'type': 'topbottompercent', 'value': args.topbottompercent}

    for competition in footballapi.get_competitions():
        logger.info(
            filtermatch.get_matches(competition, filter))


if __name__ == "__main__":
    main()
