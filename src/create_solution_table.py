import os
import sys
import csv
import sqlite3

def main():
    filename=os.path.join("solutions","schedule_871.csv")
    if len(sys.argv)>1:
        filename=sys.argv[1]
    print("loading file: ",filename)
    create_solution_table(filename)

def create_solution_table(filename):
    sql_connection = sqlite3.connect('lectures_en_lesroosters.db')
    sql_cursor = sql_connection.cursor()
    create_table_solution(filename,sql_cursor)
    create_helper_views(sql_cursor)
    sql_connection.commit()
    sql_connection.close()

def create_table_solution(filename,sql_cursor):
    sql_cursor.execute("DROP TABLE IF EXISTS solution")
    sql_cursor.execute("CREATE TABLE solution (student text, course text, activity text, room text, day text, time int)")
    sql_cursor.execute("CREATE INDEX solution_student ON solution(student)")
    sql_cursor.execute("CREATE INDEX solution_cardt ON solution(course,activity,room,day,time)")
    sql_cursor.execute("CREATE INDEX solution_rdt ON solution(room,day,time)")
    sql_cursor.execute("CREATE INDEX solution_sdt ON solution(student,day,time)")
    sql_cursor.execute("CREATE INDEX solution_sd ON solution(student,day)")
    with open(filename, 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader) # skip first (header) row
        for row in csv_reader:
            if len(row)>0:
                student=row[0]
                course=row[1]
                activity=row[2]
                room=row[3]
                day=row[4]
                time=int(row[5])
                #print(student,course,activity,room,day,time)
                sql_cursor.execute("INSERT INTO solution VALUES (?,?,?,?,?,?)",
                                   (student,course,activity,room,day,time))

def create_helper_views(sql_cursor):
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
    
if __name__ == "__main__":
    main()
