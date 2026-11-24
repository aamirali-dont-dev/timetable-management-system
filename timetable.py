# timetable.py  -  Member 3
# The Timetable keeps a list of classes.
# Rule: ALWAYS check for clashes BEFORE saving a class.

from models import ClassSession
from conflicts import check_conflicts      # Member 2's clash checker


def give_id(session, new_id):
    # A ClassSession can't be changed after it is created (Member 1's rule).
    # So to give it an ID, we make a NEW session with the same details plus the ID.
    return ClassSession(
        session.get_teacher(),
        session.get_course(),
        session.get_section_id(),
        session.get_room_id(),
        session.get_day(),
        session.get_start(),
        session.get_end(),
        new_id,
    )


class Timetable:
    def __init__(self, loaded_list=None):
        self.__sessions = []     # private list of all classes
        self.__next_id = 1       # the ID the next new class will get

        # If we loaded classes from a file, keep them
        # and continue the IDs after the highest one.
        if loaded_list is not None:
            for s in loaded_list:
                self.__sessions.append(s)
                if s.get_session_id() >= self.__next_id:
                    self.__next_id = s.get_session_id() + 1

    def get_all_sessions(self):
        return list(self.__sessions)      # a COPY, so the real list stays safe

    def find_session(self, session_id):
        for s in self.__sessions:
            if s.get_session_id() == session_id:
                return s
        return None                       # not found

    # ADD: returns a list of problems. Empty list = the class was added.
    def add_session(self, session):
        problems = check_conflicts(session, self.__sessions)
        if len(problems) > 0:
            return problems               # clash -> do not save

        new_session = give_id(session, self.__next_id)
        self.__sessions.append(new_session)
        self.__next_id = self.__next_id + 1
        return []                         # no problems

    # REMOVE: returns True if removed, False if the ID does not exist.
    def remove_session(self, session_id):
        old = self.find_session(session_id)
        if old is None:
            return False
        self.__sessions.remove(old)
        return True

    # UPDATE: returns a list of problems. Empty list = the class was updated.
    def update_session(self, session_id, new_session):
        old = self.find_session(session_id)
        if old is None:
            return ["No class found with ID " + str(session_id)]

        # Check clashes but IGNORE the old version of this class.
        problems = check_conflicts(new_session, self.__sessions, ignore_id=session_id)
        if len(problems) > 0:
            return problems               # clash -> old class stays unchanged

        self.__sessions.remove(old)                                # take out the old one
        self.__sessions.append(give_id(new_session, session_id))   # put in the new one
        return []


# ---------------- Small test (runs only when you run this file) ----------------
if __name__ == "__main__":
    from models import Teacher, Course

    faiza = Teacher("T01", "Faiza")
    ali = Teacher("T02", "Ali")
    course = Course("FIN-201", "Financial Accounting")

    def make(teacher, room, section, start, end, session_id=None):
        return ClassSession(teacher, course, section, room, "Monday", start, end, session_id)

    def show(problems):
        if len(problems) == 0:
            print("  ACCEPTED")
        else:
            print("  REJECTED")
            for p in problems:
                print("   ", p)

    tt = Timetable()

    print("1. Valid class (Faiza, R101, BSFT-3A, 09:00-10:00)")
    show(tt.add_session(make(faiza, "R101", "BSFT-3A", 540, 600)))

    print("2. Teacher clash (same teacher, same time)")
    show(tt.add_session(make(faiza, "R102", "BSFT-3B", 540, 600)))

    print("3. Room clash (same room, same time)")
    show(tt.add_session(make(ali, "R101", "BSFT-3B", 540, 600)))

    print("4. Section clash (same section, same time)")
    show(tt.add_session(make(ali, "R102", "BSFT-3A", 540, 600)))

    print("5. Partial overlap (09:30-10:30)")
    show(tt.add_session(make(faiza, "R102", "BSFT-3B", 570, 630)))

    print("6. Back-to-back (10:00-11:00) is allowed")
    show(tt.add_session(make(faiza, "R101", "BSFT-3A", 600, 660)))

    print("7. Add a different class (Ali, R102, BSFT-3B, 09:00-10:00)")
    show(tt.add_session(make(ali, "R102", "BSFT-3B", 540, 600)))

    print("8. Update class 3 to room R101 -> clash, class 3 must stay the same")
    show(tt.update_session(3, make(ali, "R101", "BSFT-3B", 540, 600)))
    print("  Class 3 is still:", tt.find_session(3))

    print("9. Update class 3 to end at 10:30 -> accepted (old version is ignored)")
    show(tt.update_session(3, make(ali, "R102", "BSFT-3B", 540, 630)))
    print("  Class 3 is now:", tt.find_session(3))

    print("10. Remove class 3, then try again")
    print("  First time:", tt.remove_session(3))
    print("  Second time:", tt.remove_session(3))

    print("11. Loaded list with IDs 3 and 7 -> the next new ID should be 8")
    loaded = [make(faiza, "R101", "BSFT-3A", 540, 600, 3),
              make(ali, "R102", "BSFT-3B", 600, 660, 7)]
    tt2 = Timetable(loaded)
    tt2.add_session(make(faiza, "R103", "BSFT-3C", 700, 760))
    for s in tt2.get_all_sessions():
        print("  ID", s.get_session_id(), "-", s)
