import os
import sqlite3

import table_reader


def main():
    data_path = os.path.join("data")
    create_data_tables(data_path)


def create_data_tables(data_path):
    sql_connection = sqlite3.connect('lectures_en_lesroosters.db')
    sql = sql_connection.cursor()
    create_table_rooms(os.path.join(data_path, "zalen.csv"), sql)
    create_table_days(os.path.join(data_path, "dagen.csv"), sql)
    create_table_timeslots(os.path.join(data_path, "tijden.csv"), sql)
    create_table_courses(os.path.join(data_path, "vakken.csv"), sql)
    create_table_students(os.path.join(
        data_path, "studenten_en_vakken.csv"), sql)
    create_helper_views(sql)
    sql_connection.commit()
    sql_connection.close()


def create_table_rooms(filename, sql):
    sql.execute("DROP TABLE IF EXISTS rooms")
    sql.execute("CREATE TABLE rooms (name text, capacity int, special text)")
    sql.execute("CREATE INDEX rooms_name ON rooms(name)")
    for row in table_reader.read_rows(filename):
        name = row[0]
        capacity = int(row[1])
        special = "" if len(row) == 2 else row[2]
        # print(name,capacity,special)
        sql.execute("INSERT INTO rooms VALUES (?,?,?)",
                    (name, capacity, special))


def create_table_days(filename, sql):
    sql.execute("DROP TABLE IF EXISTS days")
    sql.execute("CREATE TABLE days (name text)")
    sql.execute("CREATE INDEX days_name ON days(name)")
    for row in table_reader.read_rows(filename):
        name = row[0]
        # print(name)
        sql.execute("INSERT INTO days VALUES (?)",
                    (name,))


def create_table_timeslots(filename, sql):
    sql.execute("DROP TABLE IF EXISTS timeslots")
    sql.execute("CREATE TABLE timeslots (name int,cost int,special text)")
    sql.execute("CREATE INDEX timeslots_name ON timeslots(name)")
    for row in table_reader.read_rows(filename):
        name = int(row[0])
        cost = int(row[1])
        special = "" if len(row) == 2 else row[2]
        # print(name,cost,special)
        sql.execute("INSERT INTO timeslots VALUES (?,?,?)",
                    (name, cost, special))


def add_activity(sql, name, activity, max_students, expected_nr_students):
    # print(name,activity,max_students,expected_nr_students)
    sql.execute("INSERT INTO courses VALUES (?,?,?,?)",
                (name, activity, max_students, expected_nr_students))


def create_table_courses(filename, sql):
    sql.execute("DROP TABLE IF EXISTS courses")
    sql.execute(
        "CREATE TABLE courses (name text,activity text,max_students int,expected_nr_students int)")
    sql.execute("CREATE INDEX courses_name ON courses(name)")
    unlimited = 999999
    for row in table_reader.read_rows(filename):
        name = row[0]
        expected_nr_students = int(row[6])
        #------- hoorcolleges
        nr_hoorcolleges = int(row[1])
        for i in range(nr_hoorcolleges):
            add_activity(sql, name, "h"+str(i+1),
                         unlimited, expected_nr_students)
        #------- werkcolleges
        nr_werkcolleges = int(row[2])
        max_stud_werkcolleges = table_reader.convert_int(row[3], unlimited)
        for i in range(nr_werkcolleges):
            add_activity(sql, name, "w"+str(i+1),
                         max_stud_werkcolleges, expected_nr_students)
        #------- practica
        nr_practica = int(row[4])
        max_stud_practica = table_reader.convert_int(row[5], unlimited)
        for i in range(nr_practica):
            add_activity(sql, name, "p"+str(i+1),
                         max_stud_practica, expected_nr_students)


def create_table_students(filename, sql):
    sql.execute("DROP TABLE IF EXISTS students")
    sql.execute("CREATE TABLE students (name text,course text)")
    sql.execute("CREATE INDEX students_name ON students(name)")
    for row in table_reader.read_rows(filename):
        name = f"{row[1]} {row[0]}"
        for index in range(3, len(row)):
            course = row[index]
            if len(course) < 2:
                break
            # print(student,course)
            sql.execute("INSERT INTO students VALUES (?,?)",
                        (name, course))


def create_helper_views(sql):
    # all valid room and time combinations with cost
    sql.execute("DROP VIEW IF EXISTS roomslots;")
    sql.execute('''CREATE VIEW roomslots AS 
    SELECT rooms.name as room, timeslots.name as time, timeslots.cost as cost
    FROM rooms JOIN timeslots on INSTR(rooms.special,timeslots.special)>0;''')

    # all students scheduled to course activities
    sql.execute("DROP VIEW IF EXISTS student_courses;")
    sql.execute('''CREATE VIEW student_courses AS 
    SELECT students.name, students.course, courses.activity 
    FROM students JOIN courses ON students.course = courses.name;''')


if __name__ == "__main__":
    main()
