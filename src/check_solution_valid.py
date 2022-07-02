import sqlite3

def main():
    check_solution_valid()

def check_solution_valid():
    sql_connection = sqlite3.connect('lectures_en_lesroosters.db')
    sql_cursor = sql_connection.cursor()
    create_helper_views(sql_cursor)

    results = check_missing_students(sql_cursor)
    if results:
        print("missing_students:",results)

    results = check_extra_students(sql_cursor)
    if results:
        print("extra_students:",results)

    results = check_max_students_limit(sql_cursor)
    if results:
        print("max_students_limit:",results)
    
    sql_connection.commit()
    sql_connection.close()

def create_helper_views(sql_cursor):
    sql_cursor.execute("DROP VIEW IF EXISTS student_courses;")
    sql_cursor.execute('''CREATE VIEW student_courses AS 
    SELECT students.name, students.course, courses.activity 
    FROM students JOIN courses ON students.course = courses.name;''')

    sql_cursor.execute("DROP VIEW IF EXISTS student_counts_for_activity;")
    sql_cursor.execute('''CREATE VIEW student_counts_for_activity AS 
    SELECT solution.course, solution.activity, count(solution.student) as count
    FROM solution GROUP BY solution.course,solution.activity,solution.room,solution.time;''')
    
def to_string(sql_cursor):
    return [row for row in sql_cursor]
    
def check_missing_students(sql_cursor):
    return to_string(sql_cursor.execute(
    '''SELECT * FROM student_courses 
    EXCEPT 
    SELECT solution.student, solution.course, solution.activity FROM solution;'''))
    
def check_extra_students(sql_cursor):
    return to_string(sql_cursor.execute(
    '''SELECT solution.student, solution.course, solution.activity FROM solution
    EXCEPT
    SELECT * FROM student_courses;'''))

def check_max_students_limit(sql_cursor):
    return to_string(sql_cursor.execute(
    '''SELECT * FROM student_counts_for_activity 
    JOIN courses ON student_counts_for_activity.course = courses.name AND student_counts_for_activity.activity = courses.activity
    WHERE student_counts_for_activity.count > courses.max_students;'''))

if __name__ == "__main__":
    main()

