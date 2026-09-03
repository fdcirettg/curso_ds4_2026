""" Main app for the Athletes module. It creates teams, athletes, and simulates a game between them."""
from Game import Game
from Team import Team
from Sport import Sport
from Athlete import Athlete
import json
from itertools import combinations

def load_json_file(file_path):
    """ Loads a JSON file and returns the data as a Python object."""
    data = None
    with open(file_path, 'r',encoding='utf-8') as file:
        data = json.load(file)
    return data

def convert_json_to_teams(json_data):
    """ Converts JSON data into a list of Team objects."""
    teams = []
    for team_data in json_data:
        team_name = team_data['name']
        sport_name = team_data['sport']['name']
        sport_league = team_data['sport']['league']
        sport_num_players = team_data['sport']['num_players']
        print("---",team_name,sport_name,sport_league,sport_num_players)
        sport = Sport(sport_name, sport_league, sport_num_players)
        team = Team(team_name, sport)
        for athlete_data in team_data['athletes']:
            athlete_name = athlete_data['name']
            athlete_age = athlete_data['number']
            athlete = Athlete(athlete_name, athlete_age, sport_name)
            team.add_athlete(athlete)
        teams.append(team)
    return teams
    
def main():
    """ Main function to create teams, athletes, and simulate a game."""
    # Load data from JSON files
    tournament_data = load_json_file('curso_ds4_2026/Athletes/tournament.json')
    teams = convert_json_to_teams(tournament_data)
    
    # Create all possible combinations of two teams
    team_combinations = list(combinations(teams, 2))
    for local, visitor in team_combinations:
        print(f"Match: {local.name} vs {visitor.name}")
        game = Game(local, visitor)
        game.play()
        game.display()
        print("\n")
    
    # Simulate a game for each combination
    for team1, team2 in team_combinations:
        game = Game(team1, team2)
        game.play()

    #print("Tournament:", tournament_data)

if __name__ == "__main__":
    main()
