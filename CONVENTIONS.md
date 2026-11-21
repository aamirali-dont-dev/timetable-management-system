# Timetable Project: Shared Conventions

## Days
- Allowed: Monday, Tuesday, Wednesday, Thursday, Friday
- Input: any case, full name or 3-letter short form ("mon", "Monday", "MONDAY")
- Stored and displayed as the full name in title case: "Monday"

## Times
- Input: 24-hour "HH:MM" (also accept "9:00" without a leading zero)
- Stored as an int: minutes since midnight (09:30 -> 570), range 0 to 1439
- Displayed as zero-padded "HH:MM"
- End time must be later than start time; no class crosses midnight

## Identifiers (teachers, rooms, sections, course codes)
- Short codes: teacher T01, room R101, section BSFT-3A, course FIN-201
- Normalised: spaces trimmed, uppercased ("r101 " -> "R101")
- Letters, digits and hyphens only; no internal spaces; cannot be empty
- All comparisons use these codes, never names

## Names
- Course name and teacher name: free text, trimmed, cannot be empty
- Used for display only, never for conflict checks

## Scheduled class ID
- Each class gets a unique integer ID, assigned by Timetable (Member 3)
- Used to update or remove a class

## Overlap rule (Member 2)
- Two classes overlap if: same day AND start_a < end_b AND start_b < end_a
- Back-to-back (09:00-10:00 and 10:00-11:00) does NOT overlap

## Shared helpers (Member 1 provides, everyone uses)
- Convert "HH:MM" to minutes, and minutes back to "HH:MM"
- Normalise a day name
- Normalise an identifier code

## Files
- models.py      Member 1  (Teacher, Course, ClassSession, helpers)
- conflicts.py   Member 2
- timetable.py   Member 3
- storage.py, display.py   Member 4
- main.py        menu, built last

## models.py contract (final)

### Helpers (import from models)
- time_to_minutes("09:30") -> 570          raises ValueError on bad input
- minutes_to_time(570) -> "09:30"          raises ValueError if not 0-1439
- normalize_day("mon") -> "Monday"         Monday-Friday only
- normalize_code(" r101 ") -> "R101"       letters, digits, hyphens
- name_cleaner("  Faiza ") -> "Faiza"      rejects empty
- Days: list of the five valid days, in order (use for sorting)

### Classes
- Entity(code, name): get_code(), get_name()
- Teacher(teacher_id, name), inherits Entity: also get_id()
- Course(code, name), inherits Entity
- ClassSession(teacher, course, section_id, room_id, day, start, end, session_id=None)
  - teacher must be a Teacher object, course a Course object
  - start/end are ints in minutes; end must be after start
  - getters: get_teacher(), get_course(), get_section_id(), get_room_id(),
    get_day(), get_start(), get_end(), get_session_id()
  - print(session) gives a one-line summary
  - to_dict() -> plain dict; ClassSession.from_dict(d) -> ClassSession

### Rules
- Any invalid value raises ValueError. Callers catch ValueError and show the message.
- Sessions never change after creation. To update, build a NEW ClassSession,
  check it, and replace the old one only if it passes (Member 3).
- Saved dict keys: session_id, teacher_id, teacher_name, course_code,
  course_name, section_id, room_id, day, start, end