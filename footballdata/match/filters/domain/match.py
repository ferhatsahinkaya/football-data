class Match:
    def __init__(self, datetime, home_team, home_team_standing, away_team, away_team_standing):
        self.datetime = datetime
        self.homeTeam = home_team
        self.homeTeamStanding = home_team_standing
        self.awayTeam = away_team
        self.awayTeamStanding = away_team_standing

    def __str__(self):
        return '{} {}({}) - {}({})'.format(self.datetime, self.homeTeam, self.homeTeamStanding, self.awayTeam,
                                           self.awayTeamStanding)
