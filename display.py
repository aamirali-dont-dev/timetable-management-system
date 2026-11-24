#member#4
# display.py

from models import Days, Teacher, Course, ClassSession


def display_timetable(sessions):

    if not sessions:
        print("No classes available.")
        return

    sorted_sessions = sorted(
        sessions,
        key=lambda s: (Days.index(s.get_day()), s.get_start()) )

    print("\n===== UNIVERSITY TIMETABLE =====")

    for s in sorted_sessions:
        print("Session ID:", s.get_session_id())
        print(s)
        print("------------------------------")


# Small test
if __name__ == "__main__":

    teacher1 = Teacher("T01", "Faiza")
    teacher2 = Teacher("T02", "Ali")

    course1 = Course("FIN-201", "Financial Accounting")
    course2 = Course("FIN-202", "Corporate Finance")

    # sessions in an unsorted order
    s1 = ClassSession(
        teacher1, course1, "BSFT-3A", "R101",
        "Tuesday", 600, 660, 2 )

    s2 = ClassSession(
        teacher2, course2, "BSFT-3A", "R102",
        "Monday", 660, 720, 1 )

    s3 = ClassSession(
        teacher1, course2, "BSFT-3A", "R103",
        "Monday", 540, 600, 3 )

    display_timetable([s1, s2, s3])