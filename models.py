#same with this one
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

if __name__ == "__main__":
    T1 = Teacher('T01', 'Faiza')
    C1 = Course('BA101', 'Business Anayltics')
    CS1 = ClassSession(T1, C1, 'FT101', 'R101', 'Monday', 100, 135)

    print(f"Teacher: {T1.get_name()}\nCourse: {C1.get_name()}\nDay: {CS1.get_day()}, Start: {CS1.get_start()}")
    print(f"Teacher Name again: {CS1.get_teacher().get_name()} , Session: {CS1.get_session_id()}")
