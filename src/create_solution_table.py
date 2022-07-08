import os
import sys
import sqlite3

import table_reader


def main():
    filename = os.path.join("solutions", "schedule_871.csv")
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    print("loading file: ", filename)
    create_solution_table(filename)


def create_solution_table(filename):
    sql_connection = sqlite3.connect('lectures_en_lesroosters.db')
    sql = sql_connection.cursor()
    create_table_solution(filename, sql)
    create_helper_views(sql)
    sql_connection.commit()
    sql_connection.close()


def create_table_solution(filename, sql):
    sql.execute("DROP TABLE IF EXISTS solution")
    sql.execute("CREATE TABLE solution (student text, course text, activity text, room text, day text, time int)")
    for row in table_reader.read_rows(filename):
        student = row[0]
        course = row[1]
        activity = row[2]
        room = row[3]
        day = row[4]
        time = int(row[5])
        # print(student,course,activity,room,day,time)
        sql.execute("INSERT INTO solution VALUES (?,?,?,?,?,?)",
                    (student, course, activity, room, day, time))


def create_helper_views(sql):
    # all scheduled course activities with student_count
    sql.execute("DROP VIEW IF EXISTS activity_with_student_count;")
    sql.execute('''CREATE VIEW activity_with_student_count AS 
    SELECT solution.course, 
           solution.activity, 
           solution.room, solution.day, 
           solution.time, 
           count(solution.student) AS student_count
    FROM solution GROUP BY 
           solution.course, 
           solution.activity, 
           solution.room, 
           solution.day, 
           solution.time;''')

    # all roomslots with activity_count
    sql.execute("DROP VIEW IF EXISTS roomslots_with_activity_count;")
    sql.execute('''CREATE VIEW roomslots_with_activity_count AS 
    SELECT *,count() as activity_count FROM activity_with_student_count
    GROUP BY activity_with_student_count.room, 
             activity_with_student_count.day, 
             activity_with_student_count.time;''')


if __name__ == "__main__":
    main()
