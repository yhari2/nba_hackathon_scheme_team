import csv

def main():
    with open("sorted_play_by_play.txt", "r") as plays, open("readable_plays.txt", "w") as out:
        plays = csv.reader(plays, delimiter="\t")
        out = csv.writer(out, delimiter="\t", lineterminator="\n")

        for row in plays:
            tup = get_code(row)
            out.writerow([row[0], row[3], row[10], row[2], tup[0], row[6], tup[1], row[7], row[11], row[12]])


def get_code(data):
    with open("event_codes.txt", "r") as codes:
        codes = csv.reader(codes, delimiter="\t")

        for row in codes:
            if(data[2] == row[0] and data[6] == row[1]):
                return row[2], row[3]
        return "N/A", "N/A"

if __name__ == "__main__":
    main()
