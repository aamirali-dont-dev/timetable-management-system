from models import Teacher, Course, ClassSession, minutes_to_time


# Overlap rule (from CONVENTIONS.md):
# same day AND start_a < end_b AND start_b < end_a
# Back-to-back classes (10:00 end, 10:00 start) do NOT overlap.
def overlaps(a, b):
    return (
        a.get_day() == b.get_day()
        and a.get_start() < b.get_end()
        and b.get_start() < a.get_end()
    )


# Three separate checks. All of them compare codes, never names.
def teacher_clash(a, b):
    return a.get_teacher().get_code() == b.get_teacher().get_code()


def room_clash(a, b):
    return a.get_room_id() == b.get_room_id()


def section_clash(a, b):
    return a.get_section_id() == b.get_section_id()


# Short description of the existing class, used inside every message
def describe(session):
    return (
        f"{session.get_course().get_code()} on {session.get_day()} "
        f"{minutes_to_time(session.get_start())}-{minutes_to_time(session.get_end())} "
        f"(room {session.get_room_id()}, section {session.get_section_id()}, "
        f"teacher {session.get_teacher().get_code()})"
    )


def check_conflicts(candidate, existing, ignore_id=None):
    """
    Compare candidate against every session in existing.
    Returns a list of conflict messages. An empty list means no conflict.
    ignore_id: session_id to skip (used by update so the original is ignored).
    """
    messages = []

    for other in existing:
        # Skip the original entry when updating
        if ignore_id is not None and other.get_session_id() == ignore_id:
            continue

        # No time overlap means no conflict of any kind
        if not overlaps(candidate, other):
            continue

        if teacher_clash(candidate, other):
            messages.append(
                f"TEACHER CLASH: {candidate.get_teacher().get_name()} ({candidate.get_teacher().get_code()}) "
                f"is already teaching {describe(other)}"
            )

        if room_clash(candidate, other):
            messages.append(
                f"ROOM CLASH: {candidate.get_room_id()} "
                f"is already booked for {describe(other)}"
            )

        if section_clash(candidate, other):
            messages.append(
                f"SECTION CLASH: {candidate.get_section_id()} "
                f"already has {describe(other)}"
            )

    return messages


# Demo and tests for Member 2
if __name__ == "__main__":
    t1 = Teacher("T01", "Faiza")
    t2 = Teacher("T02", "Ali")
    c1 = Course("FIN-201", "Financial Accounting")
    c2 = Course("BA-101", "Business Analytics")

    # Existing class: Monday 09:00-10:00 (540-600), T01, R101, BSFT-3A, id 1
    base = ClassSession(t1, c1, "BSFT-3A", "R101", "Monday", 540, 600, 1)
    existing = [base]

    cases = [
        ("Valid class (different everything)",
         ClassSession(t2, c2, "BSFT-3B", "R102", "Monday", 540, 600), 0),
        ("Teacher clash only",
         ClassSession(t1, c2, "BSFT-3B", "R102", "Monday", 540, 600), 1),
        ("Room clash only",
         ClassSession(t2, c2, "BSFT-3B", "R101", "Monday", 540, 600), 1),
        ("Section clash only",
         ClassSession(t2, c2, "BSFT-3A", "R102", "Monday", 540, 600), 1),
        ("Partial overlap (09:30-10:30), teacher clash",
         ClassSession(t1, c2, "BSFT-3B", "R102", "Monday", 570, 630), 1),
        ("Back-to-back (10:00-11:00), accepted",
         ClassSession(t1, c1, "BSFT-3A", "R101", "Monday", 600, 660), 0),
        ("Same times but different day, accepted",
         ClassSession(t1, c1, "BSFT-3A", "R101", "Tuesday", 540, 600), 0),
        ("All three clash at once",
         ClassSession(t1, c2, "BSFT-3A", "R101", "Monday", 540, 600), 3),
    ]

    for label, candidate, expected in cases:
        result = check_conflicts(candidate, existing)
        status = "PASS" if len(result) == expected else "FAIL"
        print(f"[{status}] {label}: {len(result)} conflict(s)")
        for m in result:
            print("      ", m)

    # ignore_id: updating the original should not clash with itself
    same_slot = ClassSession(t1, c1, "BSFT-3A", "R101", "Monday", 540, 600, 1)
    print("\nUpdate with ignore_id=1:", check_conflicts(same_slot, existing, ignore_id=1))
    print("Same check without ignore_id:", len(check_conflicts(same_slot, existing)), "conflict(s)")

    # Empty timetable
    print("Empty timetable:", check_conflicts(base, []))