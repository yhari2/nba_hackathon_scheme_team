import csv

from player import Player

game = None
period = "1"
team1 = None
team2 = None
players1 = {}
players2 = {}
foul_present1 = []
foul_present2 = []


def main():
    with open('sorted_play_by_play.txt', 'r') as data:
        data = csv.reader(data, delimiter="\t")

        global game, period, team1, team2, players1, players2
        global foul_present1, foul_present2
        next(data)  # skips header

        # Iterates over plays in the data file
        for row in data:
            # This means we've reached a new game
            if(game is None or game != row[0]):
                write_game()
                game = row[0]
                reset()
                init_lineup()
            # This means we've reached a new period
            if(period != row[3]):
                period = row[3]
                for p in players1.values():
                    p.status = False
                for p in players2.values():
                    p.status = False
                init_lineup()

            # Check type of the action and handle accordingly
            if(int(row[2]) == 8):
                # Change the status of the two subbed players
                team_from_player(row[11]).get(row[11]).sub()
                team_from_player(row[11]).setdefault(row[12], Player(row[12]))
                team_from_player(row[11]).get(row[12]).sub()
            elif(int(row[2]) == 6):
                # Save players present at the time of the foul
                foul_present1 = [x for x in players1.values() if x.status]
                foul_present2 = [x for x in players2.values() if x.status]
            elif(int(row[2]) == 3):
                # Handle points for all active players when foul occurred
                if(team_from_player(row[11]) is players1):
                    for p in foul_present1:
                        p.score(int(row[7]))
                    for p in foul_present2:
                        p.score(-int(row[7]))
                elif(team_from_player(row[11]) is players2):
                    for p in foul_present2:
                        p.score(int(row[7]))
                    for p in foul_present1:
                        p.score(-int(row[7]))
            elif(int(row[2]) == 1):
                # Add points to every active player on the scoring team
                for p in team_from_player(row[11]).values():
                    if(p.status):
                        p.score(int(row[7]))
                # Subtract points from every active player on the other team
                for p in team_from_player(row[11], True).values():
                    if(p.status):
                        p.score(-int(row[7]))


# Initializes player dicts for a given period, adding and activating starters
def init_lineup():
    with open('game_lineup.txt', 'r') as lineup:
        lineups = csv.reader(lineup, delimiter="\t")

        global team1, team2, players1, players2
        seen = False
        next(lineups)
        for row in lineups:
            if(game == row[0] and period == row[1]):
                seen = True
                if(team1 is None or team1 == row[3]):
                    team1 = row[3]
                    players1.setdefault(row[2], Player(row[2]))
                    players1[row[2]].status = True
                else:
                    team2 = row[3]
                    players2.setdefault(row[2], Player(row[2]))
                    players2[row[2]].status = True
            elif(seen):
                return


# Writes the results of the current game to the result file
def write_game():
    global players1, players2
    if(game is None):
        with open("result.csv", "w") as result:
            (csv.writer(result, lineterminator="\n")
                .writerow(["Game_ID", "Player_ID", "Player_Plus/Minus"]))
    else:
        with open("result.csv", "a") as result:
            result = csv.writer(result, lineterminator="\n")
            for p in players1.values():
                result.writerow([game, p.pid, p.diff])
            for p in players2.values():
                result.writerow([game, p.pid, p.diff])


# Returns the player dict from the desired team or the other if other is True
def team_from_player(pid, other=False):
    if(pid in players1):
        return players1 if not other else players2
    else:
        return players2 if not other else players1


# Resets period, team1, team2, and the player dicts
def reset():
    global period, team1, team2, players1, players2
    period = "1"
    team1 = None
    team2 = None
    players1 = {}
    players2 = {}


# Handles initial sorting of plays to ensure correct ordering
def sort_data():
    with open("play_by_play.txt", "r") as plays, \
            open("sorted_play_by_playt.txt", "w") as out:

        plays = csv.reader(plays, delimiter="\t")
        out = csv.writer(out, delimiter="\t", lineterminator="\n")

        out.writerow(next(plays))
        sorted_rows = sorted(plays, key=lambda row:
                             (row[0], row[3], -int(row[5]), row[4], row[1]))
        for row in sorted_rows:
            out.writerow(row)


if __name__ == "__main__":
    sort_data()
    main()
