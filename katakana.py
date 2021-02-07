import csv
import random


def random_walk(reader):
    rows = [row for row in reader][1:]
    indices = list(range(len(rows)))
    random.shuffle(indices)
    for index in indices:
        row = rows[index]
        try:
            romaji, katakana = row
        except ValueError:
            print(f"Couldn't read row: {row}")
        print(katakana)
        input("Press any button to continue...")
        print(f"    {katakana} - {romaji}")
    print("")
    print("All done, good job!")


with open('katakana.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    random_walk(reader)
