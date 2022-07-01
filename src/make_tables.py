import os
import csv
import sqlite3

def create_table_rooms(filename,sql_cursor):
    sql_cursor.execute("DROP TABLE IF EXISTS rooms")
    sql_cursor.execute("CREATE TABLE rooms (name text, capacity int, special text)")
    with open(filename, 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader) # skip first (header) row
        for row in csv_reader:
            if len(row)>0:
                name=row[0]
                capacity=int(row[1])
                special="" if len(row)==2 else row[2]
                #print(name,capacity,special)
                sql_cursor.execute("INSERT INTO rooms VALUES (?,?,?)",
                                   (name, capacity, special))

def create_table_days(filename,sql_cursor):
    sql_cursor.execute("DROP TABLE IF EXISTS days")
    sql_cursor.execute("CREATE TABLE days (name text)")
    with open(filename, 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader) # skip first (header) row
        for row in csv_reader:
            if len(row)>0:
                name=row[0]
                #print(name)
                sql_cursor.execute("INSERT INTO days VALUES (?)",
                                   (name,))

def create_table_timeslots(filename,sql_cursor):
    sql_cursor.execute("DROP TABLE IF EXISTS timeslots")
    sql_cursor.execute("CREATE TABLE timeslots (name text,cost int,special text)")
    with open(filename, 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader) # skip first (header) row
        for row in csv_reader:
            if len(row)>0:
                name=row[0]
                cost=int(row[1])
                special="" if len(row)==2 else row[2]
                #print(name,cost,special)
                sql_cursor.execute("INSERT INTO timeslots VALUES (?,?,?)",
                                   (name,cost,special))

def create_table_courses(filename,sql_cursor):
    sql_cursor.execute("DROP TABLE IF EXISTS courses")
    sql_cursor.execute("CREATE TABLE courses (name text,nr_hoorcolleges int,nr_werkcolleges int,max_stud_werkcolleges int,nr_practica int,max_stud_practica int,expected_nr_students int)")
    with open(filename, 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader) # skip first (header) row
        for row in csv_reader:
            if len(row)>0:
                name=row[0]
                nr_hoorcolleges=int(row[1])
                nr_werkcolleges=int(row[2])
                max_stud_werkcolleges=999999
                try:
                    max_stud_werkcolleges=int(row[3])
                except:
                    pass
                nr_practica=int(row[4])
                max_stud_practica=999999
                try:
                    max_stud_werkcolleges=int(row[5])
                except:
                    pass
                expected_nr_students=row[6]
                #print(name,nr_hoorcolleges,nr_werkcolleges,max_stud_werkcolleges,nr_practica,max_stud_practica,expected_nr_students)
                sql_cursor.execute("INSERT INTO courses VALUES (?,?,?,?,?,?,?)",
                                   (name,nr_hoorcolleges,nr_werkcolleges,max_stud_werkcolleges,nr_practica,max_stud_practica,expected_nr_students))

def create_table_students(filename,sql_cursor):
    sql_cursor.execute("DROP TABLE IF EXISTS students")
    sql_cursor.execute("CREATE TABLE students (student text,course text)")
    with open(filename, 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader) # skip first (header) row
        for row in csv_reader:
            if len(row)>0:
                student=f"{row[1]} {row[0]}"
                for index in range(3,len(row)):
                    course=row[index]
                    if len(course)<2:
                        break
                    #print(student,course)
                    sql_cursor.execute("INSERT INTO students VALUES (?,?)",
                                   (student,course))
        
def main():
    sql_connection = sqlite3.connect('lectures_en_lesroosters.db')
    sql_cursor = sql_connection.cursor()
    data_path=os.path.join("..","data")
    create_table_rooms(os.path.join(data_path,"zalen.csv"),sql_cursor)
    create_table_days(os.path.join(data_path,"dagen.csv"),sql_cursor)
    create_table_timeslots(os.path.join(data_path,"tijden.csv"),sql_cursor)
    create_table_courses(os.path.join(data_path,"vakken.csv"),sql_cursor)
    create_table_students(os.path.join(data_path,"studenten_en_vakken.csv"),sql_cursor)
    
if __name__ == "__main__":
    main()

