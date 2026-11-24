# storage.py

import json
from models import ClassSession, Teacher, Course


def save(sessions):

    data = []

    for s in sessions:
        data.append(s.to_dict())

    try:
        with open("timetable.json", "w") as file:
            json.dump(data, file, indent=4)

        print("Timetable saved successfully!")

    except Exception as e:
        print("Error saving timetable:", e)


def load():

    sessions = []

    try:
        with open("timetable.json", "r") as file:
            data = json.load(file)

    except FileNotFoundError:
        print("File not found!")
        return []

    except Exception as e:
        print("Error loading file:", e)
        return []

    for item in data:

        try:
            s = ClassSession.from_dict(item)
            sessions.append(s)

        except Exception as e:
            print("Damaged record skipped:", e)

    return sessions


# Small test
if __name__ == "__main__":

    teacher = Teacher("T01", "Faiza")
    course = Course("FIN-201", "Financial Accounting")

    s1 = ClassSession(
        teacher, course, "BSFT-3A", "R101",
        "Monday", 540, 600, 1
    )

    s2 = ClassSession(
        teacher, course, "BSFT-3A", "R102",
        "Tuesday", 600, 660, 2
    )

    save([s1, s2])

    loaded = load()

    print("\nLoaded Timetable:")

    for s in loaded:
        print(s)