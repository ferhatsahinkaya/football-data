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
                   help='Finds matches which are to be under/over goals with at least with given chance')
parser.add_argument('-p', '--percent', dest='percent', type=int, choices=range(1, 101), required=True,
                    help='Percentage between 1 and 100 (both inclusive). Depending on query algorithm this parameter might have different meanings')
parser.add_argument('-c', '--competitions', dest='competitions', nargs='*', choices=footballapi.get_competition_ids(),
                    help='League to be searched for matches')
parser.add_argument('-ht', '--halftime', action='store_true',
                    help='Return results based on half time scores')

args = parser.parse_args()


def main():
    logger.info(args)
    if args.numberofgoals:
        filter = {'type': 'underover', 'numberofgoals': args.numberofgoals, 'percent': args.percent,
                  'halftime': args.halftime}
    else:
        filter = {'type': 'topbottom', 'percent': args.percent}

    competitions = footballapi.get_competitions()
    competitions = [competition for competition in competitions if competition['league'] in args.competitions] \
        if args.competitions is not None else competitions

    for competition in competitions:
        logger.info(filtermatch.get_matches(competition, filter))


if __name__ == "__main__":
    main()
