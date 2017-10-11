import argparse
import logging

from footballapi import footballapi
from match import filtermatch

logger = logging.getLogger()
logger.setLevel(logging.INFO)
parser = argparse.ArgumentParser(description='Finds matches according to given query')
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('-tb', '--topbottom', action='store_true',
                   help='Finds matches between top and bottom x percent teams')
group.add_argument('-uo', '--underover', dest='numberofgoals', type=int,
                   help='Finds matches which are to be under/over goals with at least given chance')
parser.add_argument('-p', '--percent', dest='percent', type=int, choices=range(1, 101), required=True,
                    help='Percentage between 1 and 100 (both inclusive)')
parser.add_argument('-c', '--competitions', dest='competitions', type=int, nargs='*', choices=footballapi.get_competition_ids(),
                    help='League to be searched for matches')

args = parser.parse_args()


def main():
    logger.info(args)
    if args.numberofgoals:
        filter = {'type': 'underover', 'numberofgoals': args.numberofgoals, 'percent': args.percent}
    else:
        filter = {'type': 'topbottom', 'percent': args.percent}

    competitions = footballapi.get_competitions()
    competitions = [competition for competition in competitions if competition['id'] in args.competitions] \
        if args.competitions is not None else competitions

    for competition in competitions:
        logger.info(filtermatch.get_matches(competition, filter))


if __name__ == "__main__":
    main()
