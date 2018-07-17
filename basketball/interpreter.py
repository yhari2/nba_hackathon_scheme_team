import csv

def main():
    with open("sorted_play_by_play.txt", "r") as plays, open("readable_plays.txt", "w") as out:
        plays = csv.reader(plays, delimiter="\t")
        out = csv.writer(out, delimiter="\t", lineterminator="\n")

        for row in plays:
            tup = get_code(row)
            if(row[2] == "1" or row[2] == "3" or row[2] == "6" or row[2] == "8"):
                out.writerow(["G: {}:{} Event: {}-{} Points: {} Player 1: {} Player 2: {}".format(row[0][:3], row[3], row[2], tup[0][:12], row[7], row[11][:3], row[12][:3])])


def get_code(data):
    with open("event_codes.txt", "r") as codes:
        codes = csv.reader(codes, delimiter="\t")

        for row in codes:
            if(data[2] == row[0] and data[6] == row[1]):
                return row[2], row[3]
        return "N/A", "N/A"


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
