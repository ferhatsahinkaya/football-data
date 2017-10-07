from .filters.strategy import topbottompercent

filter_types = {
    'topbottompercent': topbottompercent
}
def get_matches(competition, filter):
    return filter_types[filter['type']].get_matches(competition, filter)
