import csv
import random


def random_walk(reader):
    rows = [row for row in reader][1:]
    indices = list(range(len(rows)))
    random.shuffle(indices)
    for index in indices:
        row = rows[index]
        kanji, hiragana, meaning = row
        print(kanji)
        input("Press any button to continue...")
        print(f"    {kanji} - {hiragana} - {meaning}")
    print("")
    print("All done, good job!")


with open('database.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    random_walk(reader)
