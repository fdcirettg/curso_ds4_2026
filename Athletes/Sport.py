class Sport:
    """ Sport class represents a sport in a thournament"""
    max_score = {
        "Soccer":20,
        "Baseball":50,
        "Football":70,
        "Basketball":150,
        "Voleyball":3,
        "Tennis":3
    }
    def __innit__(self, sport_name, num_players, league):
        if sport_name in self.max_score:
            self.sport_name = sport_name
        else:
            raise ValueError(
                f"Sport name should be:{', '.join(self.max_score.keys())}"
            )
        