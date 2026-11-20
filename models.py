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
if __name__ == "__main__":
    tests = ["09:30", "9:00", "23:59", "0930", "25:00", "09:6", "ab:cd", "09:30:00"]
    for t in tests:
        try:
            print(t, "equals", time_to_minutes(t))
        except ValueError as e:
            print(t, "rejected:", e)

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
if __name__ == "__main__":
    tests = [570, 540, 0, 1439, -5, 1440]
    for m in tests:
        try:
            print(m, "equals", minutes_to_time(m))
        except ValueError as e:
            print(m, "rejected:", e)
    print(minutes_to_time(time_to_minutes('09:30')))


Days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
def normalize_day(self, day):
    self.day = day
    if day not in Days:
        raise ValueError("Class can only be schduled Monday through Friday")
    else:
        day.title()

def normalize_code(self, code):
    self.code = code
    if not code.strip():
        raise ValueError("Please enter a valid value")


# Base for the rest
class Teacher:
    def __init__(self, teacher_id, name):
        self.__teacher_id = teacher_id
        self.__name = name

    # Methods
    def get_id(self):
        return self.__teacher_id
    def get_name(self):
        return self.__name
    
class Course:
    def __init__(self, code, name):
        self.__code = code
        self.__name = name

    # Methods
    def get_code(self):
        return self.__code
    def get_name(self):
        return self.__name

class ClassSession:
    def __init__(self, teacher, course, section_id, room_id, day, start, end, session_id = None):
        self.__teacher = teacher
        self.__course = course
        self.__section_id = section_id
        self.__room_id = room_id
        self.__day = day
        self.__start = start
        self.__end = end
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
