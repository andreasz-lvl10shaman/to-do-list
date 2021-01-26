import sqlite3


def initDB():
    # Adatbázis és kapcsolódási pont létrehozása

    try:
        connection = sqlite3.connect("todo.db")

        # felhasznűlói nevek és jelszavak tárolására, adatbázis létrehozása

        c = connection.cursor()

        # get the count of tables with the name
        c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='userdata' ''')

        # if the count is 1, then table exists
        if c.fetchone()[0] == 1:
            print('User Table exists.')
        else:
            print('User Table does not exist.')

            try:
                connection.execute(
                    "CREATE TABLE userdata(UID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username TEXT NOT NULL, password TEXT NOT NULL);")

                connection.commit()
                print("userdata Table Created")
            except sqlite3.OperationalError:
                print("userdata Table couldn't be Created")

        # task adatbázis létrehozása

        # get the count of tables with the name
        c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='tasks' ''')

        # if the count is 1, then table exists
        if c.fetchone()[0] == 1:
            print('Tasks Table exists.')
        else:
            print('tasks Table does not exist.')

            try:
                connection.execute(
                    "CREATE TABLE tasks(TId INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, Task TEXT NOT NULL, UID INTEGER NOT NULL, done INTEGER NOT NULL);")
                connection.commit()
                print("userdata Table Created")
            except sqlite3.OperationalError:
                print("userdata Table couldn't be Created")

    # adatbázis bezárása

    finally:
        connection.close()
        print("user database closed")


def submit_user(username, password):
    # felhasnáló regisztrálása
    username = username.upper()
    try:
        user_db_conn = sqlite3.connect("todo.db")
        crsr = user_db_conn.cursor()
        crsr.execute("SELECT username FROM userdata")
        result = crsr.fetchall()
        valid = True
        for i in range(len(result)):
            if username == result[i][0]:
                valid = False
        if valid:
            user_db_conn.execute(
                "INSERT INTO userdata (username, password) VALUES ('{}', '{}')".format(username, password))
            user_db_conn.commit()
        else:
            print("username allready exists")
    finally:
        user_db_conn.close()


def Add_Task(task, id):
    # task hozzáadása felhasználó saját adatbázisához
    if task != "":
        try:
            connection = sqlite3.connect("todo.db")
            Cursor = connection.cursor()
            Cursor.execute("INSERT INTO tasks (task, UID, done) VALUES ('{}', '{}', '0')".format(task, id))
            connection.commit()

        finally:
            connection.close()


def Delete_Task(taskID):
    # task törlése felhasználó saját adatbázisából
    try:
        user_task_conn = sqlite3.connect("todo.db")

        try:
            user_task_conn.execute("DELETE FROM tasks WHERE TId = {}".format(taskID))
            user_task_conn.commit()
            print("task {} is deleted".format(taskID))
        except sqlite3.OperationalError:
            print("Data couldn't be Deleted")


    finally:
        user_task_conn.close()


def log_in_user(username, password):
    username = username.upper()
    try:
        connection = sqlite3.connect("todo.db")
        crsr = connection.cursor()
        crsr.execute("SELECT username, password FROM userdata")
        result = crsr.fetchall()
        for i in range(len(result)):
            if username == result[i][0]:
                if password == result[i][1]:
                    connection.close()
                    return True
                else:
                    return False
            else:
                return False
        print("username-password combination is not valid")
    finally:
        connection.close()


def Get_Id(username):
    try:
        conn = sqlite3.connect("todo.db")
        crsr = conn.cursor()

        crsr.execute("SELECT UID FROM userdata WHERE username = '{}'".format(username))
        conn.commit()
        id = crsr.fetchone()[0]
        return (id)

    finally:
        conn.close()


def Return_All_Tasks(id):
    try:
        connection = sqlite3.connect("todo.db")
        Cursor = connection.cursor()
        Cursor.execute(("SELECT * FROM tasks WHERE UID = '{}'".format(id)))
        result = Cursor.fetchall()
        return (result)

        connection.commit()
    finally:
        connection.close()


def Set_Done(tof, id):
    try:
        conn = sqlite3.connect("todo.db")
        crsr = conn.cursor()

        crsr.execute("UPDATE tasks SET done = '{}' WHERE TId = '{}'".format(tof, id))
        conn.commit()


    finally:
        conn.close()
