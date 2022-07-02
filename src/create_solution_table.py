import os
import sys
import csv
import sqlite3

def main():
    filename=os.path.join("..","solutions","schedule_871.csv")
    if len(sys.argv)>1:
        filename=sys.argv[1]
    print("loading file: ",filename)
    create_solution_table(filename)

def create_solution_table(filename):
    sql_connection = sqlite3.connect('lectures_en_lesroosters.db')
    sql_cursor = sql_connection.cursor()
    create_table_solution(filename,sql_cursor)
    sql_connection.commit()
    sql_connection.close()

def create_table_solution(filename,sql_cursor):
    sql_cursor.execute("DROP TABLE IF EXISTS solution")
    sql_cursor.execute("CREATE TABLE solution (student text, course text, activity text, room text, day text, time int)")
    sql_cursor.execute("CREATE INDEX solution_student ON solution(student)")
    sql_cursor.execute("CREATE INDEX solution_course ON solution(course)")
    sql_cursor.execute("CREATE INDEX solution_activity ON solution(activity)")
    sql_cursor.execute("CREATE INDEX solution_room ON solution(room)")
    sql_cursor.execute("CREATE INDEX solution_day ON solution(day)")
    sql_cursor.execute("CREATE INDEX solution_time ON solution(time)")
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

if __name__ == "__main__":
    main()

