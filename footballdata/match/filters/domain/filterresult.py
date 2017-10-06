class FilterResult:
    def __init__(self, competition, matches):
        self.competition = competition
        self.matches = matches

    def __str__(self):
        return self.competition + '\n' + '\n'.join(str(match) for match in self.matches)
