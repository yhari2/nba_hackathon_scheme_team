import csv

from player import Player

game = None
period = "1"
team1 = None
team2 = None
players1 = {}
players2 = {}


def main():
    with open('cleaned_data_periods.csv', 'r') as data:
        data = csv.reader(data)

        global game, period, team1, team2, players1, players2

        seen = 0
        per_game = 0

        # Iterates over plays in the data file
        for row in data:
            if(seen == 0):
                seen = 1
                continue
            # This means we've reached a new game
            if(game is None or game != row[1]):
                write_game()
                print(per_game)
                per_game = 0
                game = row[1]
                reset()
                init_lineup()
                print("players1: {}, players2: {}".format(len(players1.keys()), len(players2.keys())))
            # This means we've reached a new period
            if(period != row[3]):
                period = row[3]
                for p in players1.values():
                    p.status = False
                for p in players2.values():
                    p.status = False
                init_lineup()
                print("players1: {}, players2: {}".format(len(players1.keys()), len(players2.keys())))

            # Check type of the action and handle accordingly
            per_game = per_game + 1
            if(row[5] == 8):
                # Change the status of the two subbed players
                player(row[2]).get(row[6]).sub()
                player(row[2]).get(row[7]).sub()
            else:
                # Add points to every active player on the scoring team
                for p in player(row[2]).values():
                    if(p.status):
                        p.score(2)
                # Subtract points from every active player on the other team
                for p in player(row[2], True).values():
                    if(p.status):
                        p.score(-2)


# Initializes player dicts for a given period, adding and activating starters
def init_lineup():
    with open('game_lineup.txt', 'r') as lineup:
        lineups = csv.reader(lineup, delimiter="\t")

        global team1, team2, players1, players2
        first = True
        seen = False
        for row in lineups:
            if(first):
                first = False
                continue
            if(game == row[0] and period == row[1]):
                seen = True
                if(team1 is None or team1 == row[3]):
                    print("pid-team1:" + row[2])
                    team1 = row[3]
                    players1.setdefault(row[2], Player(row[2]))
                    players1[row[2]].status = True
                else:
                    print("pid-team2:" + row[2])
                    team2 = row[3]
                    players2.setdefault(row[2], Player(row[2]))
                    players2[row[2]].status = True
            elif(seen):
                print("done")
                return


# Writes the results of the current game to the result file
def write_game():
    global players1, players2
    with open("result.csv", "a") as result:
        result = csv.writer(result)
        if(game is None):
            result.writerow(["Game_ID", "Player_ID", "Player_Plus/Minus"])
        else:
            for p in players1.values():
                result.writerow([game, p.pid, p.diff])
            for p in players2.values():
                result.writerow([game, p.pid, p.diff])


# Returns the player dict from the desired team or the other if other is True
def player(team, other=False):
    if(team == team1):
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


if __name__ == "__main__":
    main()
