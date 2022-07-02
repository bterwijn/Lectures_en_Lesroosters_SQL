import sqlite3

def get_activity_gabs(sql_cursor):
    all_hours=[int(h[0]) for h in sql_cursor.execute("SELECT name FROM timeslots;")]
    days=sql_cursor.execute("SELECT group_concat(time) FROM solution GROUP BY student,day;")
    gaps=[0 for h in range(len(all_hours)-2)]
    for day in days:
        count_gaps(gaps,day[0],all_hours)
    return gaps
        
def count_gaps(gaps,day,all_hours):
    hours={int(h) for h in day.split(',')}
    if len(hours)>1:
        gap=0
        active=False
        for i in all_hours:
            if i in hours:
                active=True
                if gap>0:
                    gaps[gap-1]+=1
                    gap=0
            else:
                if active:
                    gap+=1
    return gaps
            
def test_gaps(): # some count_gaps test
    print( count_gaps([0,0,0],"9,11",[9,11,13,15,17]) )
    print( count_gaps([0,0,0],"9,13",[9,11,13,15,17]) )
    print( count_gaps([0,0,0],"9,15",[9,11,13,15,17]) )
    print( count_gaps([0,0,0],"9,17",[9,11,13,15,17]) )
    print( count_gaps([0,0,0],"11,17",[9,11,13,15,17]) )
    print( count_gaps([0,0,0],"9,13,17",[9,11,13,15,17]) )
    
if __name__ == "__main__":
    test_gaps()
