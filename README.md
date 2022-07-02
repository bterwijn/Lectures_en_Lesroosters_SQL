# Lectures_en_Lesroosters_SQL
Checks validity and computes the score of a solution to the Lectures_en_Lesroosters case using SQLite.

# valid solution example 

    python src/create_data_tables.py                                     # loads the case data in the database
    python src/create_solution_table.py solutions/schedule_871.csv       # loads a valid example solution in the database
* loading file:  solutions/schedule_871.csv

then we check and compute:

    python src/check_solution_valid.py                                   # check for invalid solution
    python src/compute_solution_score.py                                 # computes the score
* time_cost: 20
* room_capacity_cost: 334
* course_conflict_cost: 268
* gab_cost: 249
* total_cost: 871

# invalid solution example 

    python src/create_data_tables.py                                      # loads the case data in the database
    python src/create_solution_table.py solutions/schedule_871_INVALID.csv  # loads an invalid example solution in the database
* loading file:  solutions/schedule_871_INVALID.csv
   
then we check and compute:

    python src/check_solution_valid.py                                    # check for invalid solution
* ERROR: invalid_students: [('Yanick Abbing WRONG',)]
* ERROR: invalid_courses: [('Webprogrammeren en databases WRONG',)]
* ERROR: invalid_rooms: [('A1.06 WRONG',)]
* ERROR: invalid_days: [('ma WRONG',)]
* ERROR: invalid_times: [(-99,)]
* ERROR: invalid_roomslots: [('A1.06 WRONG', 15), ('C1.112', -99)]
* ERROR: missing_scheduled_students: [('Roelof Adam', 'Webprogrammeren en databases', 'h1'), ('Willibrordus Agema', 'Calculus 2', 'h1'), ('Yanick Abbing', 'Analysemethoden en -technieken', 'h1')]
* ERROR: extra_scheduled_students: [('Roelof Adam', 'Webprogrammeren en databases WRONG', 'h1'), ('Willibrordus Agema', 'Calculus 2', 'h1 WRONG'), ('Yanick Abbing WRONG', 'Analysemethoden en -technieken', 'h1')]
* ERROR: roomslots_multi_use: [('C0.110', 'di', 13), ('C0.110', 'do', 13)]
