import os
import sqlite3

import table_reader

def main():
    data_path=os.path.join("data")
    create_data_tables(data_path)
    
def create_data_tables(data_path):
    sql_connection = sqlite3.connect('lectures_en_lesroosters.db')
    sql_cursor = sql_connection.cursor()
    create_table_rooms(os.path.join(data_path,"zalen.csv"),sql_cursor)
    create_table_days(os.path.join(data_path,"dagen.csv"),sql_cursor)
    create_table_timeslots(os.path.join(data_path,"tijden.csv"),sql_cursor)
    create_table_courses(os.path.join(data_path,"vakken.csv"),sql_cursor)
    create_table_students(os.path.join(data_path,"studenten_en_vakken.csv"),sql_cursor)
    create_helper_views(sql_cursor)
    sql_connection.commit()
    sql_connection.close()

def create_table_rooms(filename,sql_cursor):
    sql_cursor.execute("DROP TABLE IF EXISTS rooms")
    sql_cursor.execute("CREATE TABLE rooms (name text, capacity int, special text)")
    sql_cursor.execute("CREATE INDEX rooms_name ON rooms(name)")
    for row in table_reader.read_rows(filename):
        name=row[0]
        capacity=int(row[1])
        special="" if len(row)==2 else row[2]
        #print(name,capacity,special)
        sql_cursor.execute("INSERT INTO rooms VALUES (?,?,?)",
                           (name, capacity, special))

def create_table_days(filename,sql_cursor):
    sql_cursor.execute("DROP TABLE IF EXISTS days")
    sql_cursor.execute("CREATE TABLE days (name text)")
    sql_cursor.execute("CREATE INDEX days_name ON days(name)")
    for row in table_reader.read_rows(filename):
        name=row[0]
        #print(name)
        sql_cursor.execute("INSERT INTO days VALUES (?)",
                           (name,))

def create_table_timeslots(filename,sql_cursor):
    sql_cursor.execute("DROP TABLE IF EXISTS timeslots")
    sql_cursor.execute("CREATE TABLE timeslots (name int,cost int,special text)")
    sql_cursor.execute("CREATE INDEX timeslots_name ON timeslots(name)")
    for row in table_reader.read_rows(filename):
        name=int(row[0])
        cost=int(row[1])
        special="" if len(row)==2 else row[2]
        #print(name,cost,special)
        sql_cursor.execute("INSERT INTO timeslots VALUES (?,?,?)",
                           (name,cost,special))

def create_table_courses(filename,sql_cursor):
    sql_cursor.execute("DROP TABLE IF EXISTS courses")
    sql_cursor.execute("CREATE TABLE courses (name text,activity text,max_students int,expected_nr_students)")
    sql_cursor.execute("CREATE INDEX courses_name ON courses(name)")
    unlimited=999999
    for row in table_reader.read_rows(filename):
        name=row[0]
        expected_nr_students=row[6]
        #------- hoorcolleges
        nr_hoorcolleges=int(row[1])
        for i in range(nr_hoorcolleges):
            sql_cursor.execute("INSERT INTO courses VALUES (?,?,?,?)",
                               (name,"h"+str(i+1),unlimited,expected_nr_students))
        #------- werkcolleges
        nr_werkcolleges=int(row[2])
        max_stud_werkcolleges=unlimited
        try:
            max_stud_werkcolleges=int(row[3])
        except:
            pass
        for i in range(nr_werkcolleges):
            sql_cursor.execute("INSERT INTO courses VALUES (?,?,?,?)",
                               (name,"w"+str(i+1),max_stud_werkcolleges,expected_nr_students))
        #------- practica
        nr_practica=int(row[4])
        max_stud_practica=unlimited
        try:
            max_stud_practica=int(row[5])
        except:
            pass
        for i in range(nr_practica):
            sql_cursor.execute("INSERT INTO courses VALUES (?,?,?,?)",
                               (name,"p"+str(i+1),max_stud_practica,expected_nr_students))
                
def create_table_students(filename,sql_cursor):
    sql_cursor.execute("DROP TABLE IF EXISTS students")
    sql_cursor.execute("CREATE TABLE students (name text,course text)")
    sql_cursor.execute("CREATE INDEX students_name ON students(name)")
    for row in table_reader.read_rows(filename):
        name=f"{row[1]} {row[0]}"
        for index in range(3,len(row)):
            course=row[index]
            if len(course)<2:
                break
            #print(student,course)
            sql_cursor.execute("INSERT INTO students VALUES (?,?)",
                                       (name,course))

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

                    
if __name__ == "__main__":
    main()

