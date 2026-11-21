# Helpers

# H1--------------time to minutes
def time_to_minutes(text):
    text = text.strip()
    if ":" not in text:
        raise ValueError("Enter a value containing ':' e.g, 09:30")
    
    parts = text.split(':')
    if len(parts) != 2:
        raise ValueError("Enter a number in format like: 00:00")
    else:
        hours, minutes = parts
        
    if not hours.isdigit() or not minutes.isdigit():
        raise ValueError("Hours and/or minutes are not all digits")

    if len(minutes) != 2:
        raise ValueError("Minutes must be in '00' format")

    hours_int, minutes_int = int(hours), int(minutes)
    if not (0 <= hours_int <= 23) or not (0 <= minutes_int <= 59):
        raise ValueError("Enter a valid time between 0-23 for hours & 0-59 for minutes")
    else:
        return hours_int * 60 + minutes_int

# Test cases for H1
"""
if __name__ == "__main__":
    tests = ["09:30", "9:00", "23:59", "0930", "25:00", "09:6", "ab:cd", "09:30:00"]
    for t in tests:
        try:
            print(t, "equals", time_to_minutes(t))
        except ValueError as e:
            print(t, "rejected:", e)
"""
# H2-------------- minutes to time
def minutes_to_time(mins):
    if not isinstance(mins, int):
        raise ValueError("Enter a number")
    elif not 0 <= mins <= 1439:
        raise ValueError("Enter a range b/w 0-1439")
    else:
        unpack = divmod(mins, 60)
        hours, minutes = unpack
        return f"{hours:02d}:{minutes:02d}"
    
# Test cases for H2
"""
if __name__ == "__main__":
    tests = [570, 540, 0, 1439, -5, 1440]
    for m in tests:
        try:
            print(m, "equals", minutes_to_time(m))
        except ValueError as e:
            print(m, "rejected:", e)
    print(minutes_to_time(time_to_minutes('09:30')))
"""

# H3-------------- Day Normalization
Days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
def normalize_day(day):
    d = day.strip().lower()

    for x in Days:
        if d == x.lower() or d == x[:3].lower():
            return x
    raise ValueError("Only Monday to Friday is Allowed")

# Test cases for H3
"""
if __name__ == "__main__":
    tests = ['Monday', 'monday', ' MON ', 'thu', 'Saturday', 'sat', 't', '']
    for n in tests:
        try:
            print(n, "equals", normalize_day(n))
        except ValueError as e:
            print(n, "rejected:", e)
"""

# H4-------------- Code Normalization

def normalize_code(code):
    cleaned = code.strip().upper()
    if len(cleaned) == 0:
        raise ValueError("Enter something, like a valid code")
    for e in cleaned:
        if not e.isalnum() and e != "-":
            raise ValueError("Invalid code entered")
    return cleaned

# Test cases for H4
"""
if __name__ == "__main__":
    tests = [' r101 ', 'bsft-3a', 'T01', '', '  ', 'R 101', 'R101!']
    for c in tests:
        try:
            print(c, "equals", normalize_code(c))
        except ValueError as e:
            print(c, "rejected:", e)
"""

# Extra Helper
def name_cleaner(text):
    cleaned = text.strip()
    if not cleaned:
        raise ValueError("Name cannot be empty")
    return cleaned

# Base for the rest
class Teacher:
    def __init__(self, teacher_id, name):
        self.__teacher_id = normalize_code(teacher_id)
        self.__name = name_cleaner(name)

    # Methods
    def get_id(self):
        return self.__teacher_id
    def get_name(self):
        return self.__name
    
class Course:
    def __init__(self, code, name):
        self.__code = normalize_code(code)
        self.__name = name_cleaner(name)

    # Methods
    def get_code(self):
        return self.__code
    def get_name(self):
        return self.__name

class ClassSession:
    def __init__(self, teacher, course, section_id, room_id, day, start, end, session_id = None):
        if not isinstance(teacher, Teacher):
            raise ValueError(f"{teacher} is not a registered Teacher")  
        self.__teacher = teacher

        if not isinstance(course, Course):
            raise ValueError(f"{course} is not a registered Course")
        self.__course = course

        self.__section_id = normalize_code(section_id)
        self.__room_id = normalize_code(room_id)
        self.__day = normalize_day(day)

        if not isinstance(start, int) or not (0 <= start <= 1439):
            raise ValueError(f"{start} Enter a digit and b/w 0-1439")
        self.__start = start

        if not isinstance(end, int) or not (0 <= end <= 1439):
                    raise ValueError(f"{end} Enter a digit and b/w 0-1439")
        self.__end = end

        # End after Start validation
        if end <= start:
            raise ValueError(f"{end} must be after {start}")
        
        if not session_id is None and not isinstance(session_id, int):
            raise ValueError(f"{session_id} must be 'None' or a number")
        self.__session_id = session_id

    # Methods
    def get_teacher(self):
        return self.__teacher

    def get_course(self):
        return self.__course

    def get_section_id(self):
        return self.__section_id

    def get_room_id(self):
        return self.__room_id

    def get_day(self):
        return self.__day

    def get_start(self):
        return self.__start

    def get_end(self):
        return self.__end

    def get_session_id(self):
        return self.__session_id

"""
Previous Test Cases

if __name__ == "__main__":
    T1 = Teacher('T01', 'Faiza')
    C1 = Course('BA101', 'Business Anayltics')
    CS1 = ClassSession(T1, C1, 'FT101', 'R101', 'Monday', 100, 135)

    print(f"Teacher: {T1.get_name()}\nCourse: {C1.get_name()}\nDay: {CS1.get_day()}, Start: {CS1.get_start()}")
    print(f"Teacher Name again: {CS1.get_teacher().get_name()} , Session: {CS1.get_session_id()}")
"""

# Constructor Validation
if __name__ == "__main__":

# VALID RUNS
    print(f"VALID RUNS")
    t = Teacher(" t01 ", "Faiza")
    c = Course("fin-201", "Financial Accounting")
    s = ClassSession(t, c, "bsft-3a", "r101", "monday", 555, 600)

    print("Teacher ID:  ", s.get_teacher().get_id())      # T01
    print("Teacher name:", s.get_teacher().get_name())    # Faiza
    print("Course code: ", s.get_course().get_code())     # FIN-201
    print("Course name: ", s.get_course().get_name())     # Financial Accounting
    print("Section:     ", s.get_section_id())            # BSFT-3A
    print("Room:        ", s.get_room_id())               # R101
    print("Day:         ", s.get_day())                   # Monday
    print("Start:       ", minutes_to_time(s.get_start()))  # 555 09:15
    print("End:         ", minutes_to_time(s.get_end()))      # 600 10:00
    print("Session ID:  ", s.get_session_id())            # None

# INVALID RUNS (using tuples to unpack clear msgs later)
    print(f"\nINVALID RUNS")
    bad_cases = [
        ("Teacher: empty name",          lambda: Teacher("T01", "   ")),
        ("Teacher: bad ID",              lambda: Teacher("T 01", "Faiza")),
        ("Course: empty name",           lambda: Course("FIN-201", "")),
        ("Course: bad code",             lambda: Course("FIN@201", "Accounts")),
        ("Session: teacher not Teacher", lambda: ClassSession("T01", c, "BSFT-3A", "R101", "Monday", 555, 600)),
        ("Session: course not Course",   lambda: ClassSession(t, "FIN-201", "BSFT-3A", "R101", "Monday", 555, 600)),
        ("Session: bad section code",    lambda: ClassSession(t, c, "BSFT 3A", "R101", "Monday", 555, 600)),
        ("Session: bad room code",       lambda: ClassSession(t, c, "BSFT-3A", "R-101!", "Monday", 555, 600)),
        ("Session: Saturday",            lambda: ClassSession(t, c, "BSFT-3A", "R101", "Saturday", 555, 600)),
        ("Session: start as text",       lambda: ClassSession(t, c, "BSFT-3A", "R101", "Monday", "09:15", 600)),
        ("Session: start negative",      lambda: ClassSession(t, c, "BSFT-3A", "R101", "Monday", -10, 600)),
        ("Session: end out of range",    lambda: ClassSession(t, c, "BSFT-3A", "R101", "Monday", 555, 1500)),
        ("Session: end equals start",    lambda: ClassSession(t, c, "BSFT-3A", "R101", "Monday", 600, 600)),
        ("Session: end before start",    lambda: ClassSession(t, c, "BSFT-3A", "R101", "Monday", 600, 540)),
        ("Session: ID as text",          lambda: ClassSession(t, c, "BSFT-3A", "R101", "Monday", 555, 600, "5")),
        ]

    for labels, attempt in bad_cases:
        try:
            attempt()
            print(f"ACCEPTED (bug!):{labels}")
        except ValueError as e:
            print(f"REJECTED {labels}: {e}")

