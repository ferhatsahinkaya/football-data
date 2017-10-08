from .filters.strategy import topbottom
from .filters.strategy import underover

filter_types = {
    'topbottom': topbottom,
    'underover': underover
}


def get_matches(competition, filter):
    return filter_types[filter['type']].get_matches(competition, filter)
