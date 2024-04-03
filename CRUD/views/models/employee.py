import sqlite3


def showallrecords():
    try:
        connect = sqlite3.connect("views/database/storage.db")
        cursor = connect.cursor()
        cursor.execute("SELECT * FROM tblemployee")
        registers = []
        for item in cursor.fetchall():
            # test = item[1]
            # print(test)
            registers.append(item)
        return registers
    except Exception as error:
        print(error)
        msg = "Error"
        return msg


def save_newemployee(name, position, office):
    try:
        connect = sqlite3.connect("views/database/storage.db")
        cursor = connect.cursor()

        if name != "" and position != "" and office != "":
            cursor.execute("INSERT INTO tblemployee(name, position, office) VALUES(?,?,?)", (name, position, office))
            connect.commit()
            connect.close()
            msg = "success"
            return msg
        else:
            msg = "failure"
            return msg
    except Exception as Error:
        print(Error)
        msg = "failure"
        return msg


def show_selectedEmployee(id):
    try:
        connect = sqlite3.connect("views/database/storage.db")
        cursor = connect.cursor()
        cursor.execute("SELECT * FROM tblemployee WHERE id =?", (id,))
        editemployees = []
        for item in cursor.fetchone():
            editemployees.append(item)
        return editemployees

    except Exception as error:
        print(error)
        msg = "Error"
        return msg


def update_newemployee(name, position, office, id):
    try:
        connect = sqlite3.connect("views/database/storage.db")
        cursor = connect.cursor()

        if name != "" and position != "" and office != "":
            cursor.execute("UPDATE tblemployee SET name =?, position =?, office =? WHERE id =?",
                           (name, position, office, id,))
            connect.commit()
            connect.close()
            msg = "success"
            return msg
        else:
            msg = "failure"
            return msg
    except Exception as Error:
        print(Error)
        msg = "failure"
        return msg


def show_deleteEmployee(id):
    try:
        connect = sqlite3.connect("views/database/storage.db")
        cursor = connect.cursor()
        cursor.execute("DELETE FROM tblemployee WHERE id =?", (id,))
        connect.commit()
        connect.close()
        msg = "success"
        return msg

    except Exception as error:
        print(error)
        msg = "Error"
        return msg