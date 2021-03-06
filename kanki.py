import csv
import random
import pathlib
import datetime
import json


EASY = "e"
GOOD = "g"
HARD = "h"
AGAIN = "a"
MASTERED = "m"

easy_factor = 1.5
good_factor = 1.2
one_hour = datetime.timedelta(seconds=1 * 60 * 60)
one_day = one_hour * 24
one_month = one_day * 30
shift = one_hour * 4


def dialog():
    response = input(
        "e - easy | g - good | h - hard | a - again | m - mastered\n"
    )
    while response not in ["e", "g", "h", "a", "m"]:
        print("    Invalid response. Try again.")
        response = input(
            "e - easy | g - good | h - hard | a - again | m - mastered"
        )
    return response


def calculate_next_time(last_seen, next_time, history, response):
    offset = next_time - last_seen
    min_offset = shift
    if offset < min_offset:
        offset = min_offset
    max_next_time = next_time + one_month
    if response == "e":
        new_offset = offset * easy_factor
        new_next_time = next_time + new_offset
    elif response == "g":
        new_offset = offset * good_factor
        new_next_time = next_time + new_offset
    elif response in ["h", "a"]:
        new_next_time = next_time + min_offset
    elif response == "m":
        new_next_time = max_next_time
    if new_next_time > max_next_time:
        new_next_time = max_next_time
    return new_next_time


def random_walk(entries):
    indices = list(range(len(entries)))
    random.shuffle(indices)
    now = datetime.datetime.today()
    for index in indices:
        entry = entries[index]
        row = entry["row"]
        last_seen = datetime.datetime.fromisoformat(entry["last_seen"])
        history = entry["history"]
        next_time = datetime.datetime.fromisoformat(entry["next_time"])
        if next_time > now:
            continue
        try:
            kanji, hiragana, katakana, meaning = row
        except ValueError:
            print(f"Couldn't read row: {row}")
        print(kanji)
        response = input("Press any button to continue (q to quit)...")
        print(f"    {kanji} - {hiragana} - {katakana} - {meaning}")
        if response == "q":
            return entries
        response = dialog()
        entries[index]["history"].append(response)
        entries[index]["last_seen"] = str(now)
        entries[index]["next_time"] = str(
            calculate_next_time(last_seen, next_time, history, response)
        )
        if response == "a":
            indices.append(index)

    print("")
    print("All done, good job!")

    return entries


def contains(entries, row):
    id_ = hash(row)
    ids = [hash(tuple(entry["row"])) for entry in entries]
    return id_ in ids


data_path = pathlib.Path("database.json")
with open("database.csv", newline="") as csvfile:
    reader = csv.reader(csvfile, delimiter=",")
    rows = [row for row in reader][1:]

now = datetime.datetime.today()
if not data_path.exists():
    print(f"Could not find {data_path}. Making it now...")
    entries = []
    for row in rows:
        row = tuple(row)
        print(f"Found new entry: {row}")
        entry = {
            "id": hash(row),
            "row": row,
            "last_seen": str(now),
            "next_time": str(now),
            "history": [],
        }
        entries.append(entry)
    with open(data_path, mode="w") as fp:
        json.dump(entries, fp)
else:
    with open(data_path, mode="r") as fp:
        entries = json.load(fp)
    for row in rows:
        row = tuple(row)
        if not contains(entries, row):
            print(f"Found new entry: {row}")
            entry = {
                "id": hash(row),
                "row": row,
                "last_seen": str(now),
                "next_time": str(now),
                "history": [],
            }
            entries.append(entry)
entries = random_walk(entries)
with open(data_path, mode="w") as fp:
    json.dump(entries, fp)
