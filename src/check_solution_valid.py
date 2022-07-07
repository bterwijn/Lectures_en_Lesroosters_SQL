import sqlite3
import activity_gap


def main():
    check_solution_valid()


def check_solution_valid():
    sql_connection = sqlite3.connect('lectures_en_lesroosters.db')
    sql = sql_connection.cursor()

    results = check_invalid_students(sql)
    if results:
        print("ERROR: invalid_students:", results)

    results = check_invalid_courses(sql)
    if results:
        print("ERROR: invalid_courses:", results)

    results = check_invalid_rooms(sql)
    if results:
        print("ERROR: invalid_rooms:", results)

    results = check_invalid_days(sql)
    if results:
        print("ERROR: invalid_days:", results)

    results = check_invalid_times(sql)
    if results:
        print("ERROR: invalid_times:", results)

    results = check_invalid_roomslots(sql)
    if results:
        print("ERROR: invalid_roomslots:", results)

    results = check_missing_scheduled_students(sql)
    if results:
        print("ERROR: missing_scheduled_students:", results)

    results = check_extra_scheduled_students(sql)
    if results:
        print("ERROR: extra_scheduled_students:", results)

    results = check_max_students_limit(sql)
    if results:
        print("ERROR: max_students_limit:", results)

    results = check_roomslots_multi_use(sql)
    if results:
        print("ERROR: roomslots_multi_use:", results)

    gaps = activity_gap.get_activity_gaps(sql)
    if (gaps[2] > 0):
        print("ERROR: there are 3-activity-gaps:", gaps[2])

    # sql_connection.commit() # nothing written
    sql_connection.close()


def to_string(sql):
    return [row for row in sql]


def check_invalid_students(sql):
    return to_string(sql.execute(
        '''SELECT DISTINCT solution.student FROM solution
        EXCEPT 
        SELECT DISTINCT students.name FROM students;'''))


def check_invalid_courses(sql):
    return to_string(sql.execute(
        '''SELECT DISTINCT solution.course FROM solution
        EXCEPT 
        SELECT DISTINCT courses.name FROM courses;'''))


def check_invalid_rooms(sql):
    return to_string(sql.execute(
        '''SELECT DISTINCT solution.room FROM solution
        EXCEPT 
        SELECT DISTINCT rooms.name FROM rooms;'''))


def check_invalid_days(sql):
    return to_string(sql.execute(
        '''SELECT DISTINCT solution.day FROM solution
        EXCEPT 
        SELECT DISTINCT days.name FROM days;'''))


def check_invalid_times(sql):
    return to_string(sql.execute(
        '''SELECT DISTINCT solution.time FROM solution
        EXCEPT 
        SELECT DISTINCT timeslots.name FROM timeslots;'''))


def check_invalid_roomslots(sql):
    return to_string(sql.execute(
        '''SELECT DISTINCT solution.room, solution.time FROM solution
        EXCEPT 
        SELECT DISTINCT roomslots.room, roomslots.time FROM roomslots;'''))


def check_missing_scheduled_students(sql):
    return to_string(sql.execute(
        '''SELECT * FROM student_courses 
        EXCEPT 
        SELECT solution.student, solution.course, solution.activity FROM solution;'''))


def check_extra_scheduled_students(sql):
    return to_string(sql.execute(
        '''SELECT solution.student, solution.course, solution.activity FROM solution
        EXCEPT
        SELECT * FROM student_courses;'''))


def check_max_students_limit(sql):
    return to_string(sql.execute(
        '''SELECT 
        activity_with_student_count.course,
        activity_with_student_count.activity,
        activity_with_student_count.room,
        activity_with_student_count.time,
        activity_with_student_count.student_count,
        courses.max_students
        FROM activity_with_student_count 
        JOIN courses ON activity_with_student_count.course   = courses.name AND 
                        activity_with_student_count.activity = courses.activity
        WHERE activity_with_student_count.student_count > courses.max_students;'''))


def check_roomslots_multi_use(sql):
    return to_string(sql.execute(
        '''SELECT room,day,time from roomslots_with_activity_count WHERE 
        roomslots_with_activity_count.activity_count>1;'''))


if __name__ == "__main__":
    main()
