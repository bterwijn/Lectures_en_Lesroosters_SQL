import sqlite3

def main():
    check_solution_valid()

def check_solution_valid():
    sql_connection = sqlite3.connect('lectures_en_lesroosters.db')
    sql_cursor = sql_connection.cursor()
    create_helper_views(sql_cursor)

    results = check_invalid_students(sql_cursor)
    if results:
        print("invalid_students:",results)

    results = check_invalid_courses(sql_cursor)
    if results:
        print("invalid_courses:",results)

    results = check_invalid_rooms(sql_cursor)
    if results:
        print("invalid_rooms:",results)

    results = check_invalid_days(sql_cursor)
    if results:
        print("invalid_days:",results)

    results = check_invalid_times(sql_cursor)
    if results:
        print("invalid_times:",results)

    results = check_invalid_roomslots(sql_cursor)
    if results:
        print("invalid_roomslots:",results)
    
    results = check_missing_scheduled_students(sql_cursor)
    if results:
        print("missing_scheduled_students:",results)

    results = check_extra_scheduled_students(sql_cursor)
    if results:
        print("extra_scheduled_students:",results)

    results = check_max_students_limit(sql_cursor)
    if results:
        print("max_students_limit:",results)

    results = check_roomslots_multi_use(sql_cursor)
    if results:
        print("roomslots_multi_use:",results)
    
    sql_connection.commit()
    sql_connection.close()

def create_helper_views(sql_cursor):
    # all valid room and time combinations with cost
    sql_cursor.execute("DROP VIEW IF EXISTS roomslots;")
    sql_cursor.execute('''CREATE VIEW roomslots AS 
    SELECT rooms.name as room, timeslots.name as time, timeslots.cost as cost
    FROM rooms JOIN timeslots on INSTR(rooms.special,timeslots.special)>0;''')

    # all students scheduled to course activities
    sql_cursor.execute("DROP VIEW IF EXISTS student_courses;")
    sql_cursor.execute('''CREATE VIEW student_courses AS 
    SELECT students.name, students.course, courses.activity 
    FROM students JOIN courses ON students.course = courses.name;''')

    # all scheduled course activities with student_count
    sql_cursor.execute("DROP VIEW IF EXISTS activity_with_student_count;")
    sql_cursor.execute('''CREATE VIEW activity_with_student_count AS 
    SELECT solution.course, solution.activity, solution.room, solution.day, solution.time, count(solution.student) AS student_count
    FROM solution GROUP BY solution.course, solution.activity, solution.room, solution.day, solution.time;''')

    # all roomslots with activity_count
    sql_cursor.execute("DROP VIEW IF EXISTS roomslots_with_activity_count;")
    sql_cursor.execute('''CREATE VIEW roomslots_with_activity_count AS 
    SELECT *,count() as activity_count FROM activity_with_student_count
    GROUP BY activity_with_student_count.room, activity_with_student_count.day, activity_with_student_count.time;''')
    
def to_string(sql_cursor):
    return [row for row in sql_cursor]

def check_invalid_students(sql_cursor):
    return to_string(sql_cursor.execute(
        '''SELECT DISTINCT solution.student FROM solution
        EXCEPT 
        SELECT DISTINCT students.name FROM students;'''))

def check_invalid_courses(sql_cursor):
    return to_string(sql_cursor.execute(
        '''SELECT DISTINCT solution.course FROM solution
        EXCEPT 
        SELECT DISTINCT courses.name FROM courses;'''))

def check_invalid_rooms(sql_cursor):
    return to_string(sql_cursor.execute(
        '''SELECT DISTINCT solution.room FROM solution
        EXCEPT 
        SELECT DISTINCT rooms.name FROM rooms;'''))

def check_invalid_days(sql_cursor):
    return to_string(sql_cursor.execute(
        '''SELECT DISTINCT solution.day FROM solution
        EXCEPT 
        SELECT DISTINCT days.name FROM days;'''))

def check_invalid_times(sql_cursor):
    return to_string(sql_cursor.execute(
        '''SELECT DISTINCT solution.time FROM solution
        EXCEPT 
        SELECT DISTINCT timeslots.name FROM timeslots;'''))

def check_invalid_roomslots(sql_cursor):
    return to_string(sql_cursor.execute(
        '''SELECT DISTINCT solution.room, solution.time FROM solution
        EXCEPT 
        SELECT DISTINCT roomslots.room, roomslots.time FROM roomslots;'''))

def check_missing_scheduled_students(sql_cursor):
    return to_string(sql_cursor.execute(
        '''SELECT * FROM student_courses 
        EXCEPT 
        SELECT solution.student, solution.course, solution.activity FROM solution;'''))
    
def check_extra_scheduled_students(sql_cursor):
    return to_string(sql_cursor.execute(
        '''SELECT solution.student, solution.course, solution.activity FROM solution
        EXCEPT
        SELECT * FROM student_courses;'''))

def check_max_students_limit(sql_cursor):
    return to_string(sql_cursor.execute(
        '''SELECT 
        activity_with_student_count.course,
        activity_with_student_count.activity,
        activity_with_student_count.room,
        activity_with_student_count.time,
        activity_with_student_count.student_count,
        courses.max_students
        FROM activity_with_student_count 
        JOIN courses ON activity_with_student_count.course = courses.name AND activity_with_student_count.activity = courses.activity
        WHERE activity_with_student_count.student_count > courses.max_students;'''))

def check_roomslots_multi_use(sql_cursor):
    return to_string(sql_cursor.execute(
        '''SELECT room,day,time from roomslots_with_activity_count WHERE roomslots_with_activity_count.activity_count>1;'''))


if __name__ == "__main__":
    main()

