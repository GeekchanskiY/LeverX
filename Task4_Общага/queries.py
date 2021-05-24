import pymysql

def connect(args):
    con = pymysql.connect(host=args.db_host, user=args.db_user, password=args.db_password, db="DMT")
    cur = con.cursor()
    return con, cur

def init(args):
    con, cur = connect(args)
    with con:
        cur.execute("CREATE TABLE if not exists Rooms(RoomID INT Primary KEY NOT NULL UNIQUE);")
        cur.execute("""CREATE TABLE if not exists Students(
            StudentID INT Primary KEY NOT NULL UNIQUE,
            sex Enum('M','F'), name VARCHAR(100),
            birthday DATETIME,
            RoomID INT,
            FOREIGN KEY (RoomID) REFERENCES Rooms(RoomID) ON DELETE CASCADE);""")

def add_rooms(args, data):
    con, cur = connect(args)
    with con:
        for i in data:
            try:
                cur.execute("INSERT Rooms(RoomID) VALUES ({});".format(int(i)))
            except pymysql.err.IntegrityError:
                continue
            con.commit()

def add_students(args, data):
    con, cur = connect(args)
    query = "INSERT Students(StudentID, sex, name, birthday, RoomID) VALUES (%s, %s, %s, %s, %s);"
    with con:
        for i in data:
            try:
                cur.execute(query, [i["id"],i["sex"],i["name"],i["birthday"],i["room"]])
            except pymysql.err.IntegrityError:
                continue
            con.commit()

def min_avg_age(args):
    con, cur = connect(args)
    query =  '''SELECT rooms.RoomID, avg(datediff(CURDATE(), students.birthday)) as Age
              FROM rooms JOIN students
              ON rooms.RoomID = students.RoomID 
              GROUP BY rooms.RoomID
              ORDER by Age ASC
              LIMIT 5'''
    with con:
        cur.execute(query)
        data = cur.fetchall()
    return data

def diff_sex(args):
    con, cur = connect(args)
    query = '''SELECT rooms.RoomID, count(DISTINCT students.sex) AS Counter
              FROM rooms JOIN students
              ON rooms.RoomID = students.RoomID
              GROUP BY rooms.RoomID
              HAVING Counter > 1'''
    with con:
        cur.execute(query)
        data = cur.fetchall()

    return data

def max_diff_age(args):
    con,cur = connect(args)
    query = '''SELECT rooms.RoomID, datediff(max(students.birthday), min(students.birthday)) as Difference 
              FROM rooms join students
              ON rooms.RoomID = students.RoomID 
              GROUP BY rooms.RoomID
              ORDER by Difference DESC
              LIMIT 5'''
    with con:
        cur.execute(query)
        data = cur.fetchall()
    return data

if __name__ == "queries":
    alive = True