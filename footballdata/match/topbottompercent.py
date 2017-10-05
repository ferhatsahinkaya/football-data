from math import ceil

from footballapi.api import FootballApi


class TopBottomPercent:
    def __init__(self):
        pass

    @staticmethod
    def before_or_equal(team, standing, position):
        return standing[team] <= position

    @staticmethod
    def after_or_equal(team, standing, position):
        return standing[team] >= position

    @staticmethod
    def get_matches(competition):
        selected_matches = []
        standing = FootballApi.get_standing(competition['id'])

        if standing:
            number_of_teams = len(standing)
            group_size = ceil(number_of_teams * 0.2)

            matches = FootballApi.get_next_week_matches(competition['id'])

            selected_matches = [match for match in matches
                                if (
                                    TopBottomPercent.before_or_equal(match['homeTeamId'], standing, group_size)
                                    and TopBottomPercent.after_or_equal(match['awayTeamId'], standing,
                                                                        number_of_teams - group_size + 1))
                                or (
                                    TopBottomPercent.before_or_equal(match['awayTeamId'], standing, group_size)
                                    and TopBottomPercent.after_or_equal(match['homeTeamId'], standing,
                                                                        number_of_teams - group_size + 1))]

        return selected_matches
