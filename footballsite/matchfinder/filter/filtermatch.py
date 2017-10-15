from footballsite.footballsite.matchfinder.filter.strategy import underover

from footballsite.matchfinder import topbottom

filter_types = {
    'topbottom': topbottom,
    'underover': underover
}


def get_matches(competition, filter):
    return filter_types[filter['type']].get_matches(competition, filter)
