import sqlite3
import activity_gap


def main():
    compute_solution_score()


def compute_solution_score():
    sql_connection = sqlite3.connect('lectures_en_lesroosters.db')
    sql = sql_connection.cursor()

    computed_time_cost = time_cost(sql)
    print("time_cost:", computed_time_cost)

    computed_room_capacity_cost = room_capacity_cost(sql)
    print("room_capacity_cost:", computed_room_capacity_cost)

    computed_activity_confict_cost = activity_confict_cost(sql)
    print("activity_confict_cost:", computed_activity_confict_cost)

    gaps = activity_gap.get_activity_gaps(sql)
    computed_gap_cost = gap_cost(gaps)
    print("gap_cost:", computed_gap_cost)

    total_cost = computed_time_cost + computed_room_capacity_cost + \
        computed_activity_confict_cost + computed_gap_cost
    print("total_cost:", total_cost)

    # sql_connection.commit() # nothing written
    sql_connection.close()


def to_int(sql):
    return int(next(sql)[0])


def time_cost(sql):
    return to_int(sql.execute(
        '''SELECT sum(cost) FROM roomslots_with_activity_count
        JOIN roomslots ON roomslots.room = roomslots_with_activity_count.room AND
                          roomslots.time = roomslots_with_activity_count.time;'''))


def room_capacity_cost(sql):
    return to_int(sql.execute(
        '''SELECT sum(student_count-capacity) FROM activity_with_student_count
        JOIN rooms ON rooms.name=activity_with_student_count.room
        WHERE student_count>capacity;'''))


def activity_confict_cost(sql):
    return to_int(sql.execute(
        '''SELECT SUM(count-1) FROM (SELECT count() as count FROM solution
        GROUP BY student,day,time) WHERE count>1;'''))


def gap_cost(gaps):
    return gaps[0]+gaps[1]*3


if __name__ == "__main__":
    main()
