import pymysql

def connect(args):
    con = pymysql.connect(host=args.db_host, user=args.db_user, password=args.db_password, db="DMT")
    cur = con.cursor()
    return con, cur

def init(args):
    con, cur = connect(args)
    with con:
        cur.execute("DROP TABLE IF EXISTS Students;")
        cur.execute("DROP TABLE IF EXISTS Rooms;")
        cur.execute("CREATE TABLE if not exists Rooms(RoomID INT Primary KEY NOT NULL UNIQUE);")
        cur.execute("CREATE TABLE if not exists Students(StudentID INT Primary KEY NOT NULL UNIQUE, sex Enum('M','F'), name VARCHAR(100),"
                    " birthday DATETIME, RoomID INT,FOREIGN KEY (RoomID) REFERENCES Rooms(RoomID) ON DELETE CASCADE);")

def add_rooms(args, data):
    con, cur = connect(args)
    with con:
        for i in data:
            cur.execute("INSERT Rooms(RoomID) VALUES ({});".format(int(i)))
            con.commit()

def add_students(args, data):
    con, cur = connect(args)
    with con:
        for i in data:

            query = "INSERT Students(StudentID, sex, name, birthday, RoomID) VALUES (%s, %s, %s, %s, %s);"
            print(query, (i["id"], i["sex"], i["name"], i["birthday"], i["room"]))
            cur.execute(query, [i["id"],i["sex"],i["name"],i["birthday"],i["room"]])
            con.commit()


if __name__ == "queries":
    alive = True